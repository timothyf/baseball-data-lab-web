from asyncio.log import logger
from django.core.cache import cache
from django.db.models import Max, OuterRef, Subquery
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd

from ..models import HallOfFameVote
from ..models import PlayerIdInfo
from ..utils import require_unified_client

PLAYER_INFO_CACHE_TIMEOUT = 60 * 60  # one hour


@api_view(['GET'])
@require_unified_client
def hall_of_fame_players(request, client):  # noqa: F841 - hall_of_fame unused
    # enrich each inducted Player with mlbam_id from PlayerIdInfo by bbref_id

    base_qs = HallOfFameVote.objects.filter(inducted=True, category='Player')
    latest_vote = base_qs.filter(bbref_id=OuterRef('bbref_id')).order_by('-year')
    players = list(
        base_qs
        .values('bbref_id')
        .annotate(
            year=Max('year'),
            voted_by=Subquery(latest_vote.values('voted_by')[:1]),
        )
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
                voted_by = row.get('voted_by')
                info = {
                    'mlbam_id': None if pd.isna(mlbam) else str(int(mlbam)),
                    'name': f"{(first or '').strip()} {(last or '').strip()}".strip(),
                    'first_name': first,
                    'last_name': last,
                    'voted_by': voted_by,
                }
            else:
                info = {}
        else:
            info = dict(info)

        p['mlbam_id'] = info.get('mlbam_id')
        p['name'] = info.get('name')
        p['first_name'] = info.get('first_name')
        p['last_name'] = info.get('last_name')
        p['voted_by'] = p.get('voted_by')

    mlbam_ids = [p['mlbam_id'] for p in players if p.get('mlbam_id')]
    cache_keys = {mid: f"player-info:{mid}" for mid in mlbam_ids}
    cached = cache.get_many(cache_keys.values())
    positions = {}
    missing_ids = []
    for mid in mlbam_ids:
        key = cache_keys[mid]
        if key in cached:
            positions[mid] = cached[key]
        else:
            missing_ids.append(mid)

    for mid in missing_ids:
        position = None
        try:
            mid_str = str(mid).strip()
            if mid_str.endswith('.0'):
                mid_str = mid_str[:-2]
            data = client.fetch_player_info(int(mid_str)) or {}
            pos = data.get('primaryPosition') or {}
            position = pos.get('name')
        except Exception:  # pragma: no cover - defensive
            position = None
        positions[mid] = position
        cache.set(cache_keys[mid], position, PLAYER_INFO_CACHE_TIMEOUT)

    for p in players:
        mlbam_id = p.get('mlbam_id')
        p['position'] = positions.get(mlbam_id)

    return Response({'players': players})
