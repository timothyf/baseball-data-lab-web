#!/usr/bin/env bash
set -euo pipefail

# ---- Supabase prod connection ----
HOST="db.tigrhjeznfdtpjfgwane.supabase.co"
DB="postgres"         # from your URL
USER="postgres"       # from your URL
PORT="5432"

# Supply your password safely (or use a .pgpass file)
export PGPASSWORD="3121018Fisher"
# Supabase requires SSL
export PGSSLMODE="require"

# (Optional) shorten psql params
PSQL="psql -h $HOST -p $PORT -U $USER -d $DB"

# ---- CSV paths (client-side; keep absolute paths) ----
TEAMS="/Users/timothyfisher/projects/Baseball/baseball-data-lab/baseball_data_lab/data/team_id_infos.csv"
VENUES="/Users/timothyfisher/projects/Baseball/baseball-data-lab/baseball_data_lab/data/mlb_venues.csv"
PEOPLE="/Users/timothyfisher/projects/Baseball/baseball-data-lab/baseball_data_lab/data/players_seed.csv"



# ---- Loads ----
$PSQL -c "\COPY team_id_infos(mlbam_team_id,abbrev,full_name,location_name,team_name,league,fg_team_id,mlbam_league_id,mlbam_division_id,bref_team_id,retrosheet_team_id,active_from,active_to) FROM '$TEAMS' WITH (FORMAT csv, HEADER true, DELIMITER ',');"

$PSQL -c "\COPY venues(mlbam_id,name,link,active,season) FROM '$VENUES' WITH (FORMAT csv, HEADER true, DELIMITER ',');"

$PSQL -c "\COPY player_id_infos(key_person,key_uuid,key_mlbam,key_retro,key_bbref,key_bbref_minors,key_fangraphs,name_last,name_first,name_given,name_suffix) FROM '$PEOPLE' WITH (FORMAT csv, HEADER true, DELIMITER ',');"

echo "✅ Seed complete against $DB@$HOST"
