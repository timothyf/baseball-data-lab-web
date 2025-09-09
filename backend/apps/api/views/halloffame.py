from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd

from ..models import HallOfFameVote
from ..models import PlayerIdInfo
from ..utils import require_unified_client


@api_view(['GET'])
@require_unified_client
def hall_of_fame_players(request, client):  # noqa: F841 - hall_of_fame unused
    # enrich each inducted Player with mlbam_id from PlayerIdInfo by bbref_id

    players = list(
        HallOfFameVote.objects
        .filter(inducted=True, category='Player')
        .values('bbref_id', 'year')
    )

    latest = {}
    for p in players:
        bid = p.get('bbref_id')
        y = p.get('year')
        cur = latest.get(bid)
        if cur is None:
            latest[bid] = p
        else:
            cy = cur.get('year')
            if cy is None or (y is not None and y > cy):
                latest[bid] = p
    players = list(latest.values())

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
        info = info_map.get(p['bbref_id'])
        if not info:
            # Fall back to a reverse lookup using the player's bbref ID.
            try:
                df = client.playerid_reverse_lookup(p['bbref_id'], key_type='bbref')
            except Exception:  # pragma: no cover - defensive
                df = None
            if df is not None and not df.empty:
                row = df.iloc[0]
                mlbam = row.get('key_mlbam')
                first = row.get('name_first')
                last = row.get('name_last')
                info = {
                    'mlbam_id': None if pd.isna(mlbam) else str(int(mlbam)),
                    'name': f"{(first or '').strip()} {(last or '').strip()}".strip(),
                    'first_name': first,
                    'last_name': last,
                }
            else:
                info = {}
        else:
            info = dict(info)

        p['mlbam_id'] = info.get('mlbam_id')
        p['name'] = info.get('name')
        p['first_name'] = info.get('first_name')
        p['last_name'] = info.get('last_name')

        # Attempt to fetch the player's primary position if an mlbam_id is
        # available. Any errors from the external client are swallowed so that
        # failure to fetch a position does not break the entire endpoint.
        mlbam_id = p.get('mlbam_id')
        position = None
        if mlbam_id:
            try:
                data = client.fetch_player_info(int(mlbam_id)) or {}
                pos = data.get('primaryPosition') or {}
                position = pos.get('name')
            except Exception:  # pragma: no cover - defensive
                position = None
        p['position'] = position

    return Response({'players': players})
