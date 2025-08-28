"""Player-related API views."""

from datetime import datetime
import logging
import re

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

from ..models import PlayerIdInfo

try:
    from baseball_data_lab.apis.unified_data_client import UnifiedDataClient
    _bdl_error = None
except Exception as exc:  # pragma: no cover - handles missing dependency
    UnifiedDataClient = None
    _bdl_error = str(exc)

logger = logging.getLogger(__name__)


@require_GET
def player_search(request):
    """Search for players by name."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)

    rows = (
        PlayerIdInfo.objects
        .filter(name_full__icontains=query)
        .order_by('name_full')
        .values('id', 'name_full', 'key_mlbam')[:10]
    )

    results = []
    for row in rows:
        key_mlbam = row.get('key_mlbam')
        if key_mlbam is not None:
            key_mlbam = str(key_mlbam)
            if key_mlbam.endswith('.0'):
                key_mlbam = key_mlbam[:-2]
        results.append(
            {
                "id": row['id'],
                "name_full": row['name_full'],
                "key_mlbam": key_mlbam,
            }
        )
    return JsonResponse(results, safe=False)


@require_GET
def player_headshot(request, player_id: int):
    """Return a player's headshot image."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    key_mlbam = (
        PlayerIdInfo.objects.filter(id=player_id)
        .values_list("key_mlbam", flat=True)
        .first()
    )
    if key_mlbam is None:
        key_mlbam = (
            PlayerIdInfo.objects.filter(key_mlbam=str(player_id))
            .values_list("key_mlbam", flat=True)
            .first()
        )
        if key_mlbam is None:
            key_mlbam = str(player_id)

    key_mlbam = str(key_mlbam)
    if key_mlbam.endswith('.0'):
        key_mlbam = key_mlbam[:-2]

    try:
        client = UnifiedDataClient()
        image_bytes = client.fetch_player_headshot(int(key_mlbam))
        return HttpResponse(image_bytes, content_type='image/png')
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def player_info(request, player_id: int):
    """Return basic information about a player."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    key_mlbam = (
        PlayerIdInfo.objects.filter(id=player_id)
        .values_list("key_mlbam", flat=True)
        .first()
    )
    if key_mlbam is None:
        key_mlbam = (
            PlayerIdInfo.objects.filter(key_mlbam=str(player_id))
            .values_list("key_mlbam", flat=True)
            .first()
        )
        if key_mlbam is None:
            key_mlbam = str(player_id)

    key_mlbam = str(key_mlbam)
    if key_mlbam.endswith('.0'):
        key_mlbam = key_mlbam[:-2]

    try:
        client = UnifiedDataClient()
        info = client.fetch_player_info(int(key_mlbam))
        team = info.get("currentTeam", {}) or {}
        pos = info.get("primaryPosition", {}) or {}
        bat = info.get("batSide", {}) or {}
        throw = info.get("pitchHand", {}) or {}
        birth_city = info.get("birthCity")
        birth_state = info.get("birthStateProvince")
        birth_country = info.get("birthCountry")
        birth_place_parts = [
            part
            for part in [birth_city, birth_state, birth_country]
            if part
        ]
        birth_place = ", ".join(birth_place_parts) if birth_place_parts else None

        data = {
            "team_id": team.get("id"),
            "team_name": team.get("name"),
            "position": pos.get("name"),
            "name": info.get("fullName"),
            "birth_date": info.get("birthDate"),
            "birth_place": birth_place,
            "height": info.get("height"),
            "weight": info.get("weight"),
            "bat_side": bat.get("description"),
            "throw_side": throw.get("description"),
        }
        return JsonResponse(data)
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def player_stats(request, player_id: int):
    """Return career statistics for a player."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    key_mlbam = (
        PlayerIdInfo.objects.filter(id=player_id)
        .values_list("key_mlbam", flat=True)
        .first()
    )
    if key_mlbam is None:
        key_mlbam = (
            PlayerIdInfo.objects.filter(key_mlbam=str(player_id))
            .values_list("key_mlbam", flat=True)
            .first()
        )
        if key_mlbam is None:
            key_mlbam = str(player_id)

    key_mlbam = str(key_mlbam)
    if key_mlbam.endswith('.0'):
        key_mlbam = key_mlbam[:-2]

    try:
        client = UnifiedDataClient()
        data = client.fetch_player_stats_career(int(key_mlbam))
        return JsonResponse(data)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "Error fetching career stats for player_id=%s, key_mlbam=%s: %s",
            player_id,
            key_mlbam,
            exc,
        )
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def league_leaders(request):
    """Return league-wide batting and pitching leaders."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    season = datetime.now().year

    try:
        client = UnifiedDataClient()
        bat_df = client.fetch_batting_leaderboards(season)
        pit_df = client.fetch_pitching_leaderboards(season)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error fetching leaderboards: %s", exc)
        return JsonResponse({'error': str(exc)}, status=500)

    def _clean_name(name):
        if not isinstance(name, str):
            return ""
        return re.sub('<[^<]+?>', '', name)

    leaders = {'batting': {}, 'pitching': {}}

    bat = bat_df.copy()
    if 'PA' in bat.columns:
        bat = bat[bat['PA'] > 50]
    for stat in ['HR', 'AVG', 'RBI', 'SB', 'SLG', 'OPS']:
        if stat in bat.columns and not bat.empty:
            sorted_df = bat.sort_values(stat, ascending=False)
            top_rows = sorted_df.head(5)
            stat_leaders = []
            for _, row in top_rows.iterrows():
                value = row.get(stat)
                if stat == 'OPS':
                    try:
                        value = f"{float(value):.3f}"
                    except (TypeError, ValueError):
                        pass
                stat_leaders.append(
                    {
                        'id': str(int(row.get('xMLBAMID'))),
                        'name': _clean_name(row.get('Name')),
                        'value': value,
                    }
                )
            leaders['batting'][stat] = stat_leaders

    pit = pit_df.copy()
    for pos_col in ('Pos', 'Position', 'POS'):
        if pos_col in pit.columns:
            pit = pit[pit[pos_col].astype(str).str.upper().str.startswith('P')]
            break

    if 'IP' in pit.columns:
        pit = pit[pit['IP'] > 50]

    for stat in ['ERA', 'SO', 'W', 'SV', 'WHIP']:
        if stat in pit.columns and not pit.empty:
            sort_ascending = stat in ('ERA', 'WHIP')
            sorted_df = pit.sort_values(stat, ascending=sort_ascending)
            top_rows = sorted_df.head(5)
            stat_leaders = []
            for _, row in top_rows.iterrows():
                value = row.get(stat)
                if stat in ('ERA', 'WHIP'):
                    try:
                        value = round(float(value), 2)
                    except (TypeError, ValueError):
                        pass
                stat_leaders.append(
                    {
                        'id': str(int(row.get('xMLBAMID'))),
                        'name': _clean_name(row.get('Name')),
                        'value': value,
                    }
                )
            leaders['pitching'][stat] = stat_leaders

    return JsonResponse(leaders)
