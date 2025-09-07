from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat


class PlayerIdInfo(models.Model):
    """Player identification information sourced from multiple providers."""

    key_person = models.CharField(max_length=20, null=True)
    key_uuid = models.CharField(max_length=40, null=True)
    key_mlbam = models.CharField(max_length=20, null=True)
    key_retro = models.CharField(max_length=20, null=True)
    key_bbref = models.CharField(max_length=20, null=True)
    key_bbref_minors = models.CharField(max_length=20, null=True)
    key_fangraphs = models.CharField(max_length=20, null=True)
    key_npb = models.CharField(max_length=20, null=True)
    name_last = models.CharField(max_length=100, null=True)
    name_first = models.CharField(max_length=100, null=True)
    name_given = models.CharField(max_length=100, null=True)
    name_suffix = models.CharField(max_length=20, null=True)
    name_full = models.GeneratedField(
        expression=Concat(F("name_first"), Value(" "), F("name_last")),
        output_field=models.CharField(max_length=200),
        db_persist=True,
    )

    class Meta:
        db_table = 'player_id_infos'

    def __str__(self) -> str:  # pragma: no cover - simple convenience method
        """Return the player's full name for admin displays."""
        return self.name_full or ""


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
    active_from = models.IntegerField(null=True)
    active_to = models.IntegerField(null=True)

    class Meta:
        db_table = 'team_id_infos'

    def __str__(self) -> str:  # pragma: no cover - simple convenience method
        """Return the team's full name for admin displays."""
        return self.full_name or ""


class Venue(models.Model):
    mlbam_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, null=True)
    active = models.BooleanField(null=True)
    season = models.IntegerField(null=True)

    class Meta:
        db_table = 'venues'

    def __str__(self) -> str:  # pragma: no cover - simple convenience method
        """Return the venue name for admin displays."""
        return self.name or ""


class HallOfFameVote(models.Model):
    bbref_id = models.CharField(max_length=20, null=True)
    year = models.IntegerField(null=True)
    voted_by = models.CharField(max_length=100, null=True)
    ballots = models.IntegerField(null=True)
    votes_needed = models.IntegerField(null=True)
    votes = models.IntegerField(null=True)
    inducted = models.BooleanField(null=True)
    category = models.CharField(max_length=50, null=True)
    needed_note = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'hall_of_fame_votes'

    def __str__(self) -> str:  # pragma: no cover - simple convenience method
        """Return the player's bbref id and year for admin displays."""
        return f"{self.bbref_id or ''} ({self.year})"
