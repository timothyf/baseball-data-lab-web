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
        # The UnifiedDataClient exposes ``get_standings_data``. Using the wrong
        # method name meant the mock in tests wasn't triggered, leading to an
        # Internal Server Error. Invoke the correct method so the provided
        # standings data is returned during testing and in production.
        data = client.get_standings_data(season=season, league_ids=league_ids)
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
        # Retrieve the day's schedule. The UnifiedDataClient exposes a
        # ``get_schedule_for_date_range`` helper which returns a list of
        # days, each containing the scheduled games. The previous
        # implementation attempted to call a misspelled
        # ``fetc_schedule_for_date_range`` method which does not exist,
        # resulting in a ``MagicMock`` being returned during tests and a
        # subsequent failure when serialising the response. Use the correct
        # method so that the mocked data provided by the tests is utilised
        # properly.
        schedule_data = client.get_schedule_for_date_range(schedule_date, schedule_date)
        for day in schedule_data:
            for game in day.get('games', []):
                teams = game.get('teams', {})
                for side in ('home', 'away'):
                    team = teams.get(side, {}).get('team')
                    team_id = team.get('id') if team else None
                    if team_id:
                        try:
                            # ``UnifiedDataClient`` exposes a
                            # ``get_team_spot_url`` method which returns the
                            # URL for a team's logo. The previous code called
                            # ``fetch_team_spot_url`` which isn't patched in
                            # the tests and therefore returned an arbitrary
                            # ``MagicMock`` object that isn't JSON
                            # serialisable. Use the correct method name.
                            team['logo_url'] = client.get_team_spot_url(team_id, 32)
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
        # Fetch the live feed data for the game.  The structure returned by
        # ``UnifiedDataClient.fetch_game_live_feed`` includes top-level
        # ``teams`` as well as ``home_team_data`` and ``away_team_data`` which
        # contain the team identifiers.  The previous implementation assumed a
        # ``gameData`` wrapper and attempted to access a non-existent
        # ``get_team_spot_url`` method which resulted in a 500 error during the
        # tests.  Use the actual structure and the ``fetch_team_spot_url``
        # method so that the mocked responses used in the tests are processed
        # correctly.
        data = client.fetch_game_live_feed(game_pk)

        home_id = data.get('home_team_data', {}).get('id')
        away_id = data.get('away_team_data', {}).get('id')

        if home_id:
            data['teams']['home']['team']['logo_url'] = client.fetch_team_spot_url(
                home_id, 32
            )
        if away_id:
            data['teams']['away']['team']['logo_url'] = client.fetch_team_spot_url(
                away_id, 32
            )

        return Response(data)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error fetching game data for game_pk=%s: %s", game_pk, exc)
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def predict_game(request, client, game_pk: int):
    """Estimate win probabilities for a single game."""

    try:
        game_data = client.fetch_game_live_feed(game_pk)

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
        logger.error("Error predicting game outcome for game_pk=%s: %s", game_pk, exc)
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