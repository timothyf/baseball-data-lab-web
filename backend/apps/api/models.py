from django.db import models


class PlayerIdInfo(models.Model):
    source = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'player_id_infos'


class TeamIdInfo(models.Model):
    mlbam_team_id = models.IntegerField(null=True)
    abbrev = models.CharField(max_length=20, null=True)
    full_name = models.CharField(max_length=100, null=True)
    location_name = models.CharField(max_length=100, null=True)
    team_name = models.CharField(max_length=100, null=True)
    league = models.CharField(max_length=50, null=True)
    fg_team_id = models.IntegerField(null=True)
    mlbam_league_id = models.IntegerField(null=True)
    mlbam_division_id = models.IntegerField(null=True)
    bref_team_id = models.CharField(max_length=20, null=True)
    retrosheet_team_id = models.CharField(max_length=20, null=True)
    active_from = models.DateField(null=True)
    active_to = models.DateField(null=True)

    class Meta:
        db_table = 'team_id_infos'
