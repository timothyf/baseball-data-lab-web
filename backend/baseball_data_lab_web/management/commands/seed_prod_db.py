# backend/core/management/commands/seed_prod_db.py
import os
import shlex
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connections

class Command(BaseCommand):
    help = "Seed the database with CSVs (runs client-side psql \\COPY)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            default="default",
            help="Database alias from settings.DATABASES (default: default)"
        )
        parser.add_argument(
            "--teams-csv",
            default=str(Path.home() / "projects/Baseball/baseball-data-lab/baseball_data_lab/data/team_id_infos.csv"),
            help="Path to team_id_infos.csv"
        )
        parser.add_argument(
            "--venues-csv",
            default=str(Path.home() / "projects/Baseball/baseball-data-lab/baseball_data_lab/data/mlb_venues.csv"),
            help="Path to mlb_venues.csv"
        )
        parser.add_argument(
            "--people-csv",
            default=str(Path.home() / "projects/Baseball/baseball-data-lab/baseball_data_lab/data/combined_people.csv"),
            help="Path to combined_people.csv"
        )
        parser.add_argument(
            "--skip-people",
            action="store_true",
            help="Skip loading player_id_infos (useful while testing)"
        )
        parser.add_argument(
            "--sslmode",
            default=None,
            help="Force PGSSLMODE (e.g., require). If omitted, inferred from host (supabase -> require)."
        )

    def handle(self, *args, **opts):
        alias = opts["database"]
        if alias not in settings.DATABASES:
            raise CommandError(f"Database alias '{alias}' not found in settings.DATABASES")

        dbs = settings.DATABASES[alias]
        name = dbs.get("NAME") or "postgres"
        user = dbs.get("USER") or os.environ.get("PGUSER") or "postgres"
        password = dbs.get("PASSWORD") or os.environ.get("PGPASSWORD") or ""
        host = dbs.get("HOST") or "localhost"
        port = str(dbs.get("PORT") or 5432)

        # Infer SSL if using Supabase (or allow override)
        sslmode = opts["sslmode"]
        if sslmode is None:
            sslmode = "require" if host.endswith(".supabase.co") else os.environ.get("PGSSLMODE", "")

        # Confirm psql is available
        try:
            subprocess.run(["psql", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            raise CommandError("psql not found on PATH. Install PostgreSQL client tools.") from e

        teams_csv = Path(opts["teams_csv"]).expanduser().resolve()
        venues_csv = Path(opts["venues_csv"]).expanduser().resolve()
        people_csv = Path(opts["people_csv"]).expanduser().resolve()

        for p in (teams_csv, venues_csv, people_csv):
            if not p.exists():
                if p is people_csv and opts["skip-people"]:
                    # allowed to skip
                    continue
                raise CommandError(f"CSV not found: {p}")

        # Build psql base command
        base_cmd = ["psql", "-h", host, "-p", port, "-U", user, "-d", name]

        # Environment for psql (avoid echoing password)
        env = os.environ.copy()
        if password:
            env["PGPASSWORD"] = password
        if sslmode:
            env["PGSSLMODE"] = sslmode

        # ——— COPY statements ———
        copy_cmds = []

        # team_id_infos
        copy_cmds.append(
            r"""\COPY team_id_infos(
                mlbam_team_id,abbrev,full_name,location_name,team_name,league,
                fg_team_id,mlbam_league_id,mlbam_division_id,bref_team_id,retrosheet_team_id,
                active_from,active_to
            ) FROM '{path}' WITH (FORMAT csv, HEADER true, DELIMITER ',');""".format(path=str(teams_csv).replace("'", "''"))
        )

        # venues
        copy_cmds.append(
            r"""\COPY venues(
                mlbam_id,name,link,active,season
            ) FROM '{path}' WITH (FORMAT csv, HEADER true, DELIMITER ',');""".format(path=str(venues_csv).replace("'", "''"))
        )

        # player_id_infos
        if not opts["skip-people"]:
            # Your CSV has an extra 'key_npb' column you want to ignore.
            # Two approaches:
            # (A) If the CSV header order matches but includes key_npb, you can stage & insert.
            # (B) Or pre-trim with csvkit externally.
            #
            # Here we do a TEMP staging + INSERT to skip key_npb safely, regardless of order.
            staging_sql = f"""
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'pg_temp' AND tablename = 'player_id_infos_staging') THEN
        -- no-op
    END IF;
END$$;

CREATE TEMP TABLE IF NOT EXISTS player_id_infos_staging (
  key_person text,
  key_uuid text,
  key_mlbam text,
  key_retro text,
  key_bbref text,
  key_bbref_minors text,
  key_fangraphs text,
  key_npb text,                -- extra column present in CSV
  name_last text,
  name_first text,
  name_given text,
  name_suffix text
);

TRUNCATE TABLE player_id_infos_staging;

\\COPY player_id_infos_staging FROM '{str(people_csv).replace("'", "''")}' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

INSERT INTO player_id_infos (
  key_person,key_uuid,key_mlbam,key_retro,key_bbref,key_bbref_minors,key_fangraphs,
  name_last,name_first,name_given,name_suffix
)
SELECT
  NULLIF(key_person,''),
  NULLIF(key_uuid,''),
  NULLIF(key_mlbam,''),
  NULLIF(key_retro,''),
  NULLIF(key_bbref,''),
  NULLIF(key_bbref_minors,''),
  NULLIF(key_fangraphs,''),
  NULLIF(name_last,''),
  NULLIF(name_first,''),
  NULLIF(name_given,''),
  NULLIF(name_suffix,'')
FROM player_id_infos_staging;
"""
            copy_cmds.append(staging_sql)

        # Execute each COPY with a separate psql call (clean logs, clear errors)
        for sql in copy_cmds:
            # Use -v ON_ERROR_STOP=1 so psql fails on first error
            cmd = base_cmd + ["-v", "ON_ERROR_STOP=1", "-c", sql]
            # Avoid printing the SQL (contains paths)
            self.stdout.write(self.style.NOTICE(f"Running: psql -h {host} -p {port} -U {user} -d {name} -c <COPY...>"))
            try:
                subprocess.run(cmd, env=env, check=True)
            except subprocess.CalledProcessError as e:
                raise CommandError(f"Seeding failed while running COPY.\nError code: {e.returncode}") from e

        self.stdout.write(self.style.SUCCESS(f"✅ Seed complete against {name}@{host}:{port} (alias: {alias})"))
