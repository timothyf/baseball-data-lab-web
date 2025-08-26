from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache
from django.urls import URLPattern
import logging
import re
logger = logging.getLogger(__name__)

from .models import PlayerIdInfo, TeamIdInfo, Venue

STANDINGS_CACHE_TIMEOUT = 60 * 60  # one hour


def _get_cached_standings(client, season, league_ids="103,104"):
    """Return standings data using cache to avoid redundant API calls."""
    cache_key = f"standings:{season}:{league_ids}"
    data = cache.get(cache_key)
    if data is None:
        data = client.get_standings_data(season=season, league_ids=league_ids)
        cache.set(cache_key, data, STANDINGS_CACHE_TIMEOUT)
    return data

try:
    from baseball_data_lab.apis.unified_data_client import UnifiedDataClient
    _bdl_error = None
except Exception as exc:  # pragma: no cover - handles missing dependency
    UnifiedDataClient = None
    _bdl_error = str(exc)


@require_GET
def list_api_endpoints(request):
    from . import urls as api_urls
    endpoints = []
    # Map endpoint names to query parameters they accept.
    query_params = {
        'api-schedule': ['date'],
        'api-player-search': ['q'],
        'api-team-search': ['q'],
        'api-team-record': ['season'],
    }

    for pattern in api_urls.urlpatterns:
        if isinstance(pattern, URLPattern):
            route = pattern.pattern._route
            display = re.sub(r'<[^:>]+:([^>]+)>', r'{\1}', route)
            params = list(pattern.pattern.converters.keys())
            endpoints.append(
                {
                    'name': pattern.name,
                    'path': f'/api/{display}',
                    'template': f'/api/{route}',
                    'params': params,
                    'query_params': query_params.get(pattern.name, []),
                }
            )
    return JsonResponse({'endpoints': endpoints})


@require_GET
def schedule(request):
    """Return schedule data for a given date."""
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'date parameter is required'}, status=400)
    try:
        schedule_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)
    try:
        client = UnifiedDataClient()
        schedule = client.get_schedule_for_date_range(schedule_date, schedule_date)
        for day in schedule:
            for game in day.get('games', []):
                teams = game.get('teams', {})
                for side in ('home', 'away'):
                    team = teams.get(side, {}).get('team')
                    team_id = team.get('id') if team else None
                    if team_id:
                        try:
                            team['logo_url'] = client.get_team_spot_url(team_id, 32)
                        except Exception:  # pragma: no cover - defensive
                            team['logo_url'] = None
        return JsonResponse(schedule, safe=False)
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def game_data(request, game_pk: int):
    """Return detailed data for a single game."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)
    try:
        client = UnifiedDataClient()
        data = client.get_game_data(game_pk)
        # Pull additional boxscore details for summary information
        try:
            boxscore = client.get_game_boxscore_data(game_pk)
            data.setdefault('liveData', {})['boxscore'] = boxscore
        except Exception:  # pragma: no cover - downstream service failure
            pass
        data['home_team_data']['logo_url'] = client.get_team_spot_url(data['home_team_data']['id'], 32)
        data['away_team_data']['logo_url'] = client.get_team_spot_url(data['away_team_data']['id'], 32)
        return JsonResponse(data, safe=False)
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def predict_game(request, game_pk: int):
    """Estimate win probabilities for a single game.

    The implementation uses a very lightweight heuristic based on current
    team winning percentages fetched from the standings endpoint.  It is not
    intended to be a full featured predictive model but provides reasonable
    sample output for the frontend.
    """
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    try:
        client = UnifiedDataClient()
        game_data = client.get_game_data(game_pk)

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

        return JsonResponse({'home': home_prob, 'away': away_prob})
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def standings(request):
    """Return standings data for the current season."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)
    try:
        client = UnifiedDataClient()
        season = datetime.now().year
        data = _get_cached_standings(client, season, "103,104")
        return JsonResponse(data, safe=False)
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def news(request):
    """Return a small set of recent league news headlines."""
    news_items = [
        {
            "title": "Opening Day is around the corner",
            "url": "https://www.mlb.com/news",
        },
        {
            "title": "Top prospect makes big league debut",
            "url": "https://www.mlb.com/news",
        },
        {
            "title": "Pitching duel ends in walk-off win",
            "url": "https://www.mlb.com/news",
        },
    ]
    return JsonResponse(news_items, safe=False)


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
    """Return a player's headshot image.

    ``player_id`` may be either the internal ``PlayerIdInfo`` primary key or a
    raw MLBAM player id.  This flexibility allows the frontend schedule view,
    which only knows MLBAM ids, to link directly to this endpoint.
    """

    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    # Look up the MLBAM id from our database when possible.  If the provided id
    # isn't found, fall back to treating it as an MLBAM id directly.
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
    """Return basic information about a player.

    ``player_id`` may be either the internal ``PlayerIdInfo`` primary key or a
    raw MLBAM player id. The response includes the player's team id, team
    name, and primary position.
    """

    if UnifiedDataClient is None:
        return JsonResponse(
            {'error': 'baseball-data-lab library is not installed'}, status=500
        )

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
    """Return career statistics for a player.

    ``player_id`` may be either the internal ``PlayerIdInfo`` primary key or a
    raw MLBAM player id. The response includes career batting and pitching
    statistics as returned by ``UnifiedDataClient.fetch_player_stats_career``.
    """

    if UnifiedDataClient is None:
        return JsonResponse(
            {'error': 'baseball-data-lab library is not installed'}, status=500
        )

    # Resolve MLBAM id similar to ``player_info``
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
        logger.error("Error fetching career stats for player_id=%s, key_mlbam=%s: %s", player_id, key_mlbam, exc)
        return JsonResponse({'error': str(exc)}, status=500)

@require_GET
def team_search(request):
    """Search for teams by name."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)

    rows = (
        TeamIdInfo.objects
        .filter(full_name__icontains=query)
        .order_by('full_name')
        .values('id', 'full_name', 'mlbam_team_id')[:10]
    )

    results = []
    for row in rows:
        mlbam_team_id = row.get('mlbam_team_id')
        if mlbam_team_id is not None:
            mlbam_team_id = str(mlbam_team_id)
        results.append(
            {
                'id': row['id'],
                'full_name': row['full_name'],
                'mlbam_team_id': mlbam_team_id,
            }
        )
    return JsonResponse(results, safe=False)


@require_GET
def team_info(request, mlbam_team_id: int):
    """Return basic team information.

    ``team_id`` may be either the MLBAM team id or the internal primary key.
    The response includes location, abbreviation, and venue information when
    available.
    """

    fields = ['id', 'full_name', 'mlbam_team_id', 'location_name', 'abbrev']
    row = (
        TeamIdInfo.objects
        .filter(mlbam_team_id=mlbam_team_id, active_to__isnull=True)
        .values(*fields)
        .first()
    )

    mlbam_team_id_value = row.get('mlbam_team_id')
    if mlbam_team_id_value is not None:
        row['mlbam_team_id'] = str(mlbam_team_id_value)

    venue_id = None
    if UnifiedDataClient is not None:
        try:
            client = UnifiedDataClient()
            team_data = client.fetch_team(int(mlbam_team_id_value or team_id))
            venue = team_data.get('venue') or {}
            venue_id = venue.get('id')
        except Exception:  # pragma: no cover - defensive
            venue_id = None

    if venue_id is not None:
        row['venue_id'] = str(venue_id)
        venue_row = (
            Venue.objects
            .filter(mlbam_id=venue_id)
            .values('mlbam_id', 'name', 'link', 'active', 'season')
            .first()
        )
        if venue_row:
            if venue_row.get('mlbam_id') is not None:
                venue_row['mlbam_id'] = str(venue_row['mlbam_id'])
            row['venue'] = venue_row
    else:
        row['venue_id'] = None

    return JsonResponse(row)


@require_GET
def team_logo(request, mlbam_team_id: int):
    """Return a team's logo image."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    mlbam_team_id = str(mlbam_team_id)

    try:
        client = UnifiedDataClient()
        logo_url = client.get_team_logo_url(int(mlbam_team_id))
        return HttpResponse(logo_url, content_type='text/plain')
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def team_record(request, mlbam_team_id: int):
    """Return a team's record for a given season."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    if mlbam_team_id is None:
        return JsonResponse({'error': 'Team not found'}, status=404)

    season_str = request.GET.get('season')
    if season_str is None:
        season_str = str(datetime.now().year)

    try:
        season = int(season_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid season'}, status=400)

    try:
        client = UnifiedDataClient()
        record = client.get_team_record_for_season(season, int(mlbam_team_id))
        return JsonResponse(record, safe=False)
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def team_recent_schedule(request, mlbam_team_id: int):
    """Return the previous and next five games for a team."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    try:
        
        client = UnifiedDataClient()
        logger.info("Fetching recent schedule for mlbam_team_id=%s", mlbam_team_id)
        schedule = client.get_recent_schedule_for_team(int(mlbam_team_id))
        return JsonResponse(schedule, safe=False)
    except ValueError as ve:
        logger.error("ValueError in team_recent_schedule: %s", ve)
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Unexpected error in team_recent_schedule: %s", exc)
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def team_roster(request, mlbam_team_id: int):
    """Return the current roster for a team."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    season = datetime.now().year

    try:
        client = UnifiedDataClient()
        roster = client.fetch_active_roster(int(mlbam_team_id), year=season)
        return JsonResponse(roster, safe=False)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Unexpected error in team_roster: %s", exc)
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

    # Batting leaders
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

    # Pitching leaders
    pit = pit_df.copy()

    # Keep only pitchers (handle possible column name variants)
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


@require_GET
def team_leaders(request, mlbam_team_id: int):
    """Return basic batting and pitching leaders for a team.

    Leaders include batting HR, AVG, RBI and pitching ERA, SO using
    ``UnifiedDataClient`` leaderboards filtered for the specified team.
    """
    logger.info("Fetching team leaders for mlbam_team_id=%s", mlbam_team_id)
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    team_row = (
        TeamIdInfo.objects.filter(mlbam_team_id=mlbam_team_id)
        .values('abbrev')
        .first()
    )
    if team_row is None:
        return JsonResponse({'error': 'Team not found'}, status=404)

    abbrev = team_row.get('abbrev')
    season = datetime.now().year
    logger.info("Using team abbrev=%s for mlbam_team_id=%s", abbrev, mlbam_team_id)
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

    # Batting leaders
    bat = bat_df[bat_df.get('TeamNameAbb') == abbrev]
    if 'PA' in bat.columns:
        bat = bat[bat['PA'] > 50]
    for stat in ['HR', 'AVG', 'RBI', 'SB', 'SLG', 'OPS']:
        if stat in bat.columns and not bat.empty:
            row = bat.sort_values(stat, ascending=False).iloc[0]
            leaders['batting'][stat] = {
                'id': str(int(row.get('xMLBAMID'))),
                'name': _clean_name(row.get('Name')),
                'value': row.get(stat),
            }

    # Pitching leaders
    pit = pit_df[pit_df.get('TeamNameAbb') == abbrev]

    # Keep only pitchers (handle possible column name variants)
    for pos_col in ('Pos', 'Position', 'POS'):
        if pos_col in pit.columns:
            pit = pit[pit[pos_col].astype(str).str.upper().str.startswith('P')]
            break

    if 'IP' in pit.columns:
        pit = pit[pit['IP'] > 20]

    if 'ERA' in pit.columns and not pit.empty:
        row = pit.sort_values('ERA').iloc[0]
        leaders['pitching']['ERA'] = {
            'id': str(int(row.get('xMLBAMID'))),
            'name': _clean_name(row.get('Name')),
            'value': row.get('ERA'),
        }
    if 'SO' in pit.columns and not pit.empty:
        row = pit.sort_values('SO', ascending=False).iloc[0]
        leaders['pitching']['SO'] = {
            'id': str(int(row.get('xMLBAMID'))),
            'name': _clean_name(row.get('Name')),
            'value': row.get('SO'),
        }
        if 'G' in pit.columns and not pit.empty:
            row = pit.sort_values('G', ascending=False).iloc[0]
            leaders['pitching']['G'] = {
            'id': str(int(row.get('xMLBAMID'))),
            'name': _clean_name(row.get('Name')),
            'value': row.get('G'),
            }
        if 'W' in pit.columns and not pit.empty:
            row = pit.sort_values('W', ascending=False).iloc[0]
            leaders['pitching']['W'] = {
                'id': str(int(row.get('xMLBAMID'))),
                'name': _clean_name(row.get('Name')),
                'value': row.get('W'),
            }
        if 'SV' in pit.columns and not pit.empty:
            row = pit.sort_values('SV', ascending=False).iloc[0]
            leaders['pitching']['SV'] = {
                'id': str(int(row.get('xMLBAMID'))),
                'name': _clean_name(row.get('Name')),
                'value': row.get('SV'),
            }
    logger.info("Team leaders for mlbam_team_id=%s: %s", mlbam_team_id, leaders)
    return JsonResponse(leaders)
