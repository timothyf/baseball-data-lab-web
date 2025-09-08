
"""Player-related API views."""

from datetime import datetime
import logging
import math
import re
import requests

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from ..models import PlayerIdInfo
from ..utils import require_unified_client
from ..serializers import (
    PlayerSearchQuerySerializer,
    PlayerSearchResultSerializer,
    PlayerInfoSerializer,
    LeagueLeadersSerializer,
)

logger = logging.getLogger(__name__)


def _replace_non_finite(obj):
    """Recursively replace NaN and infinite floats with ``None``.

    ``json.dumps`` with ``allow_nan=False`` (the default used by DRF) will raise
    ``ValueError`` if the data structure contains ``float('nan')`` or infinite
    values.  MLB's APIs occasionally return such values, so we sanitize the
    response before returning it to the client.
    """

    if isinstance(obj, float):
        return None if not math.isfinite(obj) else obj
    if isinstance(obj, dict):
        return {k: _replace_non_finite(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_replace_non_finite(v) for v in obj]
    return obj


@extend_schema(
    parameters=[PlayerSearchQuerySerializer],
    responses=PlayerSearchResultSerializer(many=True),
)
@api_view(['GET'])
def player_search(request):
    """Search for players by name."""
    query = request.GET.get('q', '').strip()
    if not query:
        return Response([])

    rows = (
        PlayerIdInfo.objects
        .filter(name_full__icontains=query)
        .order_by('name_full')
        .values('id', 'name_full', 'key_mlbam')[:10]
    )

    # Gather MLBAM ids to fetch team data in a single API call
    mlbam_ids = []
    normalized_rows = []
    for row in rows:
        key_mlbam = row.get('key_mlbam')
        if key_mlbam is not None:
            key_mlbam = str(key_mlbam)
            if key_mlbam.endswith('.0'):
                key_mlbam = key_mlbam[:-2]
            mlbam_ids.append(key_mlbam)
        normalized_rows.append({
            "id": row['id'],
            "name_full": row['name_full'],
            "key_mlbam": key_mlbam,
        })

    team_lookup = {}
    if mlbam_ids:
        try:
            resp = requests.get(
                "https://statsapi.mlb.com/api/v1/people",
                params={"personIds": ",".join(mlbam_ids)},
                timeout=5,
            )
            if resp.ok:
                people = resp.json().get("people") or []
                for person in people:
                    pid = str(person.get("id"))
                    team = (person.get("currentTeam") or {}).get("name")
                    team_lookup[pid] = team
        except Exception:  # pragma: no cover - network failure
            pass

    results = []
    for row in normalized_rows:
        results.append({
            "id": row["id"],
            "name_full": row["name_full"],
            "key_mlbam": row["key_mlbam"],
            "team_name": team_lookup.get(row["key_mlbam"]),
        })

    return Response(results)


@extend_schema(responses={(200, 'image/png'): OpenApiTypes.BINARY})
@api_view(['GET'])
@require_unified_client
def player_headshot(request, client, player_id: int):
    """Return a player's headshot image."""

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
        image_bytes = client.fetch_player_headshot(int(key_mlbam))
        return HttpResponse(image_bytes, content_type='image/png')
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error fetching player headshot: %s", exc)
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=PlayerInfoSerializer)
@api_view(['GET'])
@require_unified_client
def player_info(request, client, player_id: int):
    """Return basic information about a player."""

    try:
        logger.info("Fetching info for player_id=%s", player_id)
        info = client.fetch_player_info(int(player_id))
        team = info.get("currentTeam", {}) or {}
        pos = info.get("primaryPosition", {}) or {}
        bat = info.get("batSide", {}) or {}
        throw = info.get("pitchHand", {}) or {}

        logger.info("Processing draft info for player_id=%s", player_id)
        drafts = info.get("drafts") or []
        draft = {}
        if isinstance(drafts, list) and drafts:
            first = drafts[0] or {}
            if isinstance(first, dict):
                draft = first

        draft_team = draft.get("team") or {}
        draft_data = {
            "year": draft.get("year"),
            "round": draft.get("pickRound"),
            "pick": draft.get("roundPickNumber"),
            "overall": draft.get("pickNumber"),
            "team_id": draft_team.get("id"),
            "team_name": draft_team.get("name"),
            "school": draft.get("school"),
        } if draft else None

        logger.info("Set draft data for player_id=%s: %s", player_id, draft_data)

        birth_city = info.get("birthCity")
        birth_state = info.get("birthStateProvince")
        birth_country = info.get("birthCountry")
        birth_place_parts = [
            part
            for part in [birth_city, birth_state, birth_country]
            if part
        ]
        birth_place = ", ".join(birth_place_parts) if birth_place_parts else None
        mlb_debut_date = info.get("mlbDebutDate")

        data = {
            "team_id": team.get("id"),
            "team_name": team.get("name"),
            "position": pos.get("name"),
            "name": info.get("fullName"),
            "full_name": info.get("fullFMLName"),
            "birth_date": info.get("birthDate"),
            "birth_place": birth_place,
            "height": info.get("height"),
            "weight": info.get("weight"),
            "bat_side": bat.get("description"),
            "throw_side": throw.get("description"),
            "draft": draft_data,
            "mlb_debut_date": mlb_debut_date,
        }
        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def player_stats(request, client, player_id: int):
    """Return career statistics for a player."""

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
        data = client.fetch_player_stats_career(int(key_mlbam))
        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "Error fetching career stats for player_id=%s, key_mlbam=%s: %s",
            player_id,
            key_mlbam,
            exc,
        )
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def player_splits(request, client, player_id: int):
    """Return batting and pitching splits for a player."""
    logger.info("Fetching splits for player_id=%s", player_id)
    season_param = request.GET.get('season')
    try:
        season = int(season_param) if season_param else datetime.now().year
    except (TypeError, ValueError):
        season = datetime.now().year

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

    # def _df_to_records(df):
    #     try:
    #         return (
    #             df.reset_index()
    #             .rename(columns={"Split": "split"})
    #             .drop(columns=["Row"], errors="ignore")
    #             .to_dict(orient="records")
    #         )
    #     except Exception:  # pragma: no cover - defensive
    #         return []

    try:
        logger.info(
            "Fetching batting splits for player_id=%s, key_mlbam=%s", player_id, key_mlbam
        )
        bat_json = client.fetch_batting_splits(int(key_mlbam), season)
        logger.info("Fetching pitching splits for player_id=%s", player_id)
        pit_json = client.fetch_pitching_splits(int(key_mlbam), season)

        monthly_bat = []
        monthly_pit = []
        try:
            monthly_url = (
                f"https://statsapi.mlb.com/api/v1/people/{key_mlbam}"
                f"?hydrate=stats(group=[hitting,pitching],type=byMonth,season={season})"
            )
            logger.info(
                "Fetching monthly splits for player_id=%s, url=%s", player_id, monthly_url
            )
            resp = requests.get(monthly_url, timeout=10)
            stats = resp.json().get("people", [{}])[0].get("stats", [])
            for group in stats:
                display = group.get("group", {}).get("displayName")
                splits = group.get("splits", [])
                if display == "hitting":
                    monthly_bat = splits
                elif display == "pitching":
                    monthly_pit = splits
        except Exception as exc:  # pragma: no cover - defensive
            logger.error(
                "Error fetching monthly splits for player_id=%s: %s", player_id, exc
            )

        monthly_bat.sort(key=lambda s: int(s.get("month", 0)))
        monthly_pit.sort(key=lambda s: int(s.get("month", 0)))

        data = {
            "batting": bat_json,
            "pitching": pit_json,
            "monthly": {"batting": monthly_bat, "pitching": monthly_pit},
        }
        data = _replace_non_finite(data)
        logger.info(
            "Fetched splits for player_id=%s, key_mlbam=%s", player_id, key_mlbam
        )
        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "Error fetching splits for player_id=%s, key_mlbam=%s: %s",
            player_id,
            key_mlbam,
            exc,
        )
        return Response({"error": str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def player_gamelog(request, client, player_id: int):
    """Return game log data for a player."""
    logger.info("Fetching game log for player_id=%s", player_id)

    stat_type = request.GET.get('stat_type', 'hitting')
    season_param = request.GET.get('season')
    try:
        season = int(season_param) if season_param else datetime.now().year
    except (TypeError, ValueError):
        season = datetime.now().year

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
        data = client.fetch_player_gamelog(int(key_mlbam), stat_type, season)
        logger.info(
            "Fetched game log for player_id=%s, key_mlbam=%s", player_id, key_mlbam
        )
        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "Error fetching game log for player_id=%s, key_mlbam=%s: %s",
            player_id,
            key_mlbam,
            exc,
        )
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def player_statcast_batter_data(request, client, player_id: int):
    """Return Statcast data for a batter over a date range."""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if not start_date or not end_date:
        return Response({'error': 'start_date and end_date are required'}, status=400)

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
        data = client.fetch_statcast_batter_data(
            int(key_mlbam), start_date, end_date
        )
        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "Error fetching Statcast batter data for player_id=%s, key_mlbam=%s: %s",
            player_id,
            key_mlbam,
            exc,
        )
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def player_statcast_pitcher_data(request, client, player_id: int):
    """Return Statcast data for a pitcher over a date range."""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if not start_date or not end_date:
        return Response({'error': 'start_date and end_date are required'}, status=400)

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
        data = client.fetch_statcast_pitcher_data(
            int(key_mlbam), start_date, end_date
        )
        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "Error fetching Statcast pitcher data for player_id=%s, key_mlbam=%s: %s",
            player_id,
            key_mlbam,
            exc,
        )
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=LeagueLeadersSerializer)
@api_view(['GET'])
@require_unified_client
def league_leaders(request, client):
    """Return league-wide batting and pitching leaders."""

    season = datetime.now().year

    try:
        bat_df = client.fetch_batting_leaderboards(season)
        pit_df = client.fetch_pitching_leaderboards(season)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error fetching leaderboards: %s", exc)
        return Response({'error': str(exc)}, status=500)

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
        # Include pitchers who have thrown at least 50 innings.  The previous
        # implementation used a strict greater-than comparison which excluded
        # players right at the threshold, causing the leaderboards to omit
        # valid entries (e.g., a pitcher with exactly 50 IP).  Use ``>=`` so
        # the filtering logic matches the expectations of the tests and common
        # statistical cutoffs.
        pit = pit[pit['IP'] >= 50]

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

    return Response(leaders)
