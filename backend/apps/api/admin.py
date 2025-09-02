from django.contrib import admin

from .models import PlayerIdInfo, TeamIdInfo, Venue

@admin.register(PlayerIdInfo)
class PlayerIdInfoAdmin(admin.ModelAdmin):
    """Admin configuration for PlayerIdInfo."""

    list_display = (
        "key_person",
        "key_uuid",
        "key_mlbam",
        "key_retro",
        "key_bbref",
        "key_bbref_minors",
        "key_fangraphs",
        "key_npb",
        "name_last",
        "name_first",
        "name_given",
        "name_suffix",
        "name_full",
    )


@admin.register(TeamIdInfo)
class TeamIdInfoAdmin(admin.ModelAdmin):
    """Admin configuration for TeamIdInfo."""

    list_display = (
        "mlbam_team_id",
        "abbrev",
        "full_name",
        "location_name",
        "team_name",
        "league",
        "fg_team_id",
        "mlbam_league_id",
        "mlbam_division_id",
        "bref_team_id",
        "retrosheet_team_id",
        "active_from",
        "active_to",
    )


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """Admin configuration for Venue."""

    list_display = (
        "mlbam_id",
        "name",
        "link",
        "active",
        "season",
    )
