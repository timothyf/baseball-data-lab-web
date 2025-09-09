from rest_framework import serializers
# This module defines Django REST Framework serializers that serve as the API contract
# for the Baseball Data Lab backend. They validate input payloads and shape output
# representations for players, teams, league leaders, and related entities.
#
# Use these serializers in DRF views/viewsets to:
# - Validate incoming request data (query params and JSON bodies).
# - Serialize domain objects or dicts into consistent API responses.
# - Decouple internal data models from public API schemas.
# - Provide a single source of truth for API documentation and validation behavior.

"""
Serializers for the public API surface of the Baseball Data Lab backend.

Overview:
- Player search/query and result shapes.
- Player profile details, including draft information.
- League leader representations for batting and pitching metrics.
- Team search and team details, including venue metadata.
- News item summaries.

Notes:
- Fields with allow_null=True accept explicit null values in request/response payloads.
- Nested serializers (e.g., 'draft' within PlayerInfo) encapsulate related structures.
- DictField containers are used where keys represent metric names and values are lists of entries.
"""


# PlayerSearchQuerySerializer
"""
Validates the query parameters for player search.

Fields:
- q (str, optional): Free-text search term to match player names or identifiers.
"""


# PlayerSearchResultSerializer
"""
Represents a single player entry returned from a search result.

Fields:
- id (int): Internal player identifier.
- name_full (str): Player's full display name.
- key_mlbam (str | null): MLBAM player key, if known.
- team_name (str | null): Current or last known team display name.
"""


# DraftInfoSerializer
"""
Draft metadata for a player.

Fields:
- year (int | null): Draft year.
- round (str | null): Draft round (may contain supplemental or lettered round info).
- pick (int | null): Pick number within the round.
- overall (int | null): Overall selection number across all rounds.
- team_id (int | null): Internal identifier of the drafting team.
- team_name (str | null): Display name of the drafting team.
"""


# PlayerInfoSerializer
"""
Public-facing player profile details.

Fields:
- team_id (int | null): Internal identifier of the player's current team.
- team_name (str | null): Display name of the player's current team.
- position (str | null): Primary position (e.g., "P", "SS", "CF").
- name (str | null): Player's full display name.
- birth_date (str | null): Birthdate in ISO or human-readable format.
- birth_place (str | null): Birthplace (city, state/province, country).
- height (str | null): Height (formatted string, e.g., "6'2"").
- weight (str | null): Weight (formatted string or numeric-as-string, e.g., "205").
- bat_side (str | null): Batting handedness ("R", "L", "S").
- throw_side (str | null): Throwing handedness ("R", "L").
- draft (DraftInfoSerializer | null): Nested draft information, if available.
"""


# LeagueLeaderEntrySerializer
"""
Represents a single leaderboard entry for a specific metric.

Fields:
- id (str): Identifier for the entity (commonly player ID).
- name (str): Display name (commonly player name).
- value (str): Metric value as a string (formatted for display).
"""


# LeagueLeadersSerializer
"""
Container for league leaders across batting and pitching categories.

Fields:
- batting (dict[str, list[LeagueLeaderEntrySerializer]]):
    Mapping of batting metric keys (e.g., "HR", "AVG") to ordered lists of leaders.
- pitching (dict[str, list[LeagueLeaderEntrySerializer]]):
    Mapping of pitching metric keys (e.g., "ERA", "SO") to ordered lists of leaders.
"""


# TeamSearchResultSerializer
"""
Represents a single team entry returned from a team search.

Fields:
- id (int): Internal team identifier.
- full_name (str): Team's full display name.
- mlbam_team_id (str | null): MLBAM team identifier, if available.
"""


# TeamInfoSerializer
"""
Public-facing team details and related venue information.

Fields:
- id (int): Internal team identifier.
- full_name (str): Team's full display name.
- mlbam_team_id (str | null): MLBAM team identifier.
- location_name (str | null): City/region of the team.
- abbrev (str | null): Short team abbreviation (e.g., "LAD").
- venue_id (str | null): Identifier for the home venue, if tracked.
- venue (dict, optional): Additional venue metadata (shape may vary by source).
"""


# NewsItemSerializer
"""
Represents a short-form news item or article reference.

Fields:
- title (str): Headline or title of the news item.
- url (str): Absolute URL to the news content.
"""



class PlayerSearchQuerySerializer(serializers.Serializer):
    q = serializers.CharField(required=False)


class PlayerSearchResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name_full = serializers.CharField()
    key_mlbam = serializers.CharField(allow_null=True)
    team_name = serializers.CharField(allow_null=True)


class DraftInfoSerializer(serializers.Serializer):
    year = serializers.IntegerField(allow_null=True)
    round = serializers.CharField(allow_null=True)
    pick = serializers.IntegerField(allow_null=True)
    overall = serializers.IntegerField(allow_null=True)
    team_id = serializers.IntegerField(allow_null=True)
    team_name = serializers.CharField(allow_null=True)


class PlayerInfoSerializer(serializers.Serializer):
    team_id = serializers.IntegerField(allow_null=True)
    team_name = serializers.CharField(allow_null=True)
    position = serializers.CharField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    birth_date = serializers.CharField(allow_null=True)
    birth_place = serializers.CharField(allow_null=True)
    height = serializers.CharField(allow_null=True)
    weight = serializers.CharField(allow_null=True)
    bat_side = serializers.CharField(allow_null=True)
    throw_side = serializers.CharField(allow_null=True)
    draft = DraftInfoSerializer(allow_null=True, required=False)


class LeagueLeaderEntrySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    value = serializers.CharField()


class LeagueLeadersSerializer(serializers.Serializer):
    batting = serializers.DictField(
        child=serializers.ListSerializer(child=LeagueLeaderEntrySerializer())
    )
    pitching = serializers.DictField(
        child=serializers.ListSerializer(child=LeagueLeaderEntrySerializer())
    )


class TeamSearchResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    mlbam_team_id = serializers.CharField(allow_null=True)


class TeamInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    mlbam_team_id = serializers.CharField(allow_null=True)
    location_name = serializers.CharField(allow_null=True)
    abbrev = serializers.CharField(allow_null=True)
    venue_id = serializers.CharField(allow_null=True)
    venue = serializers.DictField(required=False)


class NewsItemSerializer(serializers.Serializer):
    title = serializers.CharField()
    url = serializers.CharField()
