from rest_framework import serializers


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
