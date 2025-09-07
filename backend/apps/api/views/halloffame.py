from rest_framework.decorators import api_view

from ..models import HallOfFameVote
from ..models import PlayerIdInfo


@api_view(['GET'])
def hall_of_fame_players(request):
    # enrich each inducted Player with mlbam_id from PlayerIdInfo by bbref_id

    players = list(
        HallOfFameVote.objects
        .filter(inducted=True, category='Player')
        .values('bbref_id', 'year')
    )

    bbref_ids = [p['bbref_id'] for p in players if p['bbref_id']]
    mlbam_map = dict(
        PlayerIdInfo.objects
        .filter(key_bbref__in=bbref_ids)
        .values_list('key_bbref', 'mlbam_id')
    )

    for p in players:
        p['mlbam_id'] = mlbam_map.get(p['bbref_id'])

    return {'players': players}





                # ("bbref_id", models.CharField(max_length=20, null=True)),
                # ("year", models.IntegerField(null=True)),
                # ("voted_by", models.CharField(max_length=100, null=True)),
                # ("ballots", models.IntegerField(null=True)),
                # ("votes_needed", models.IntegerField(null=True)),
                # ("votes", models.IntegerField(null=True)),
                # ("inducted", models.BooleanField(null=True)),
                # ("category", models.CharField(max_length=50, null=True)),
                # ("needed_note", models.CharField(max_length=255, null=True)),