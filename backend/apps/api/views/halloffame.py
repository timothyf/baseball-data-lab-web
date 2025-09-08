from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import HallOfFameVote
from ..models import PlayerIdInfo


@api_view(['GET'])
def hall_of_fame_players(request):  # noqa: F841 - hall_of_fame unused
    # enrich each inducted Player with mlbam_id from PlayerIdInfo by bbref_id

    players = list(
        HallOfFameVote.objects
        .filter(inducted=True, category='Player')
        .values('bbref_id', 'year')
    )

    bbref_ids = [p['bbref_id'] for p in players if p['bbref_id']]
    info_map = {
        bbref: {
            'mlbam_id': mlbam,
            'name': name,
            'first_name': first,
            'last_name': last,
        }
        for bbref, mlbam, name, first, last in PlayerIdInfo.objects
        .filter(key_bbref__in=bbref_ids)
        .values_list('key_bbref', 'key_mlbam', 'name_full', 'name_first', 'name_last')
    }

    for p in players:
        info = info_map.get(p['bbref_id'], {})
        p['mlbam_id'] = info.get('mlbam_id')
        p['name'] = info.get('name')
        p['first_name'] = info.get('first_name')
        p['last_name'] = info.get('last_name')

    return Response({'players': players})





                # ("bbref_id", models.CharField(max_length=20, null=True)),
                # ("year", models.IntegerField(null=True)),
                # ("voted_by", models.CharField(max_length=100, null=True)),
                # ("ballots", models.IntegerField(null=True)),
                # ("votes_needed", models.IntegerField(null=True)),
                # ("votes", models.IntegerField(null=True)),
                # ("inducted", models.BooleanField(null=True)),
                # ("category", models.CharField(max_length=50, null=True)),
                # ("needed_note", models.CharField(max_length=255, null=True)),