from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamIdInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mlbam_team_id", models.IntegerField(null=True)),
                ("abbrev", models.CharField(max_length=20, null=True)),
                ("full_name", models.CharField(max_length=100, null=True)),
                ("location_name", models.CharField(max_length=100, null=True)),
                ("team_name", models.CharField(max_length=100, null=True)),
                ("league", models.CharField(max_length=50, null=True)),
                ("fg_team_id", models.IntegerField(null=True)),
                ("mlbam_league_id", models.IntegerField(null=True)),
                ("mlbam_division_id", models.IntegerField(null=True)),
                ("bref_team_id", models.CharField(max_length=20, null=True)),
                ("retrosheet_team_id", models.CharField(max_length=20, null=True)),
                ("active_from", models.DateField(null=True)),
                ("active_to", models.DateField(null=True)),
            ],
            options={
                "db_table": "team_id_infos",
            },
        ),
    ]
