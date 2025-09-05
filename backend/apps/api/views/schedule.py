"""Schedule-related API views."""

from datetime import datetime
import logging

from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from ..utils import require_unified_client

logger = logging.getLogger(__name__)

STANDINGS_CACHE_TIMEOUT = 60 * 60  # one hour


def _get_cached_standings(client, season, league_ids="103,104"):
    """Return standings data using cache to avoid redundant API calls."""
    logger.info("Fetching standings for season=%s, league_ids=%s", season, league_ids)
    cache_key = f"standings:{season}:{league_ids}"
    data = cache.get(cache_key)
    if data is None:
        data = client.fetch_standings_data(season=season, league_ids=league_ids)
        cache.set(cache_key, data, STANDINGS_CACHE_TIMEOUT)
    return data


@extend_schema(
    parameters=[
        OpenApiParameter('date', OpenApiTypes.DATE, OpenApiParameter.QUERY),
    ],
    responses=OpenApiTypes.OBJECT,
)
@api_view(['GET'])
@require_unified_client
def schedule(request, client):
    """Return schedule data for a given date."""
    date_str = request.GET.get('date')
    if not date_str:
        return Response({'error': 'date parameter is required'}, status=400)
    try:
        schedule_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=400)
    try:
        schedule_data = client.fetc_schedule_for_date_range(schedule_date, schedule_date)
        for day in schedule_data:
            for game in day.get('games', []):
                teams = game.get('teams', {})
                for side in ('home', 'away'):
                    team = teams.get(side, {}).get('team')
                    team_id = team.get('id') if team else None
                    if team_id:
                        try:
                            team['logo_url'] = client.fetch_team_spot_url(team_id, 32)
                        except Exception:  # pragma: no cover - defensive
                            team['logo_url'] = None
        return Response(schedule_data)
    except Exception as exc:  # pragma: no cover - defensive
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def game_data(request, client, game_pk: int):
    """Return detailed data for a single game."""
    try:
        data = client.fetch_game_live_feed(game_pk)
        data['gameData']['teams']['home']['logo_url'] = client.get_team_spot_url(
            data['gameData']['teams']['home']['id'], 32
        )
        data['gameData']['teams']['away']['logo_url'] = client.get_team_spot_url(
            data['gameData']['teams']['away']['id'], 32
        )
        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def predict_game(request, client, game_pk: int):
    """Estimate win probabilities for a single game."""

    try:
        game_data = client.get_game_live_feed(game_pk)

        home_id = game_data.get('home_team_data', {}).get('id')
        away_id = game_data.get('away_team_data', {}).get('id')

        season = datetime.now().year
        standings = _get_cached_standings(client, season, "103,104")
        win_pct = {}
        for record in standings:
            for team_rec in record.get('teamRecords', []):
                team = team_rec.get('team', {})
                tid = team.get('id')
                pct_str = team_rec.get('winningPercentage')
                try:
                    win_pct[tid] = float(pct_str)
                except (TypeError, ValueError):
                    continue

        home_pct = win_pct.get(home_id, 0.5)
        away_pct = win_pct.get(away_id, 0.5)

        if home_pct + away_pct == 0:
            home_prob = 0.5
        else:
            home_prob = home_pct / (home_pct + away_pct)
        away_prob = 1.0 - home_prob

        return Response({'home': home_prob, 'away': away_prob})
    except Exception as exc:  # pragma: no cover - defensive
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def standings(request, client):
    """Return standings data for the current season."""
    try:
        season = datetime.now().year
        data = _get_cached_standings(client, season, "103,104")
        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        return Response({'error': str(exc)}, status=500)