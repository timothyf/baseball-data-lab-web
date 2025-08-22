from datetime import datetime
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
import logging
logger = logging.getLogger(__name__)

from .models import PlayerIdInfo, TeamIdInfo

try:
    from baseball_data_lab.apis.unified_data_client import UnifiedDataClient
    _bdl_error = None
except Exception as exc:  # pragma: no cover - handles missing dependency
    UnifiedDataClient = None
    _bdl_error = str(exc)


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
def standings(request):
    """Return standings data for the current season."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)
    try:
        client = UnifiedDataClient()
        season = datetime.now().year
        data = client.get_standings_data(season=season, league_ids="103,104")
        return JsonResponse(data, safe=False)
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


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
        return JsonResponse({"error": "Player not found"}, status=404)

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
    """Return basic team information by MLBAM team ID."""
    row = (
        TeamIdInfo.objects
        .filter(mlbam_team_id=mlbam_team_id)
        .values('id', 'full_name', 'mlbam_team_id')
        .first()
    )

    if row is None:
        return JsonResponse({'error': 'Team not found'}, status=404)

    mlbam_team_id_value = row.get('mlbam_team_id')
    if mlbam_team_id_value is not None:
        row['mlbam_team_id'] = str(mlbam_team_id_value)

    return JsonResponse(row)


@require_GET
def team_logo(request, team_id: int):
    """Return a team's logo image."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    mlbam_team_id = team_id
    # mlbam_team_id = (
    #     TeamIdInfo.objects.filter(id=team_id)
    #     .values_list('mlbam_team_id', flat=True)
    #     .first()
    # )

    if mlbam_team_id is None:
        return JsonResponse({'error': 'Team not found'}, status=404)

    mlbam_team_id = str(mlbam_team_id)

    try:
        client = UnifiedDataClient()
        logo_url = client.get_team_logo_url(int(mlbam_team_id))
        return HttpResponse(logo_url, content_type='text/plain')
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)


@require_GET
def team_record(request, team_id: int):
    """Return a team's record for a given season."""
    logger.info("team_record called with team_id=%s", team_id)
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    mlbam_team_id = (
        TeamIdInfo.objects.filter(id=team_id)
        .values_list('mlbam_team_id', flat=True)
        .first()
    )

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
def team_recent_schedule(request, team_id: int):
    """Return the previous and next five games for a team."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    mlbam_team_id = (
        TeamIdInfo.objects.filter(id=team_id)
        .values_list('mlbam_team_id', flat=True)
        .first()
    )

    logger.info("team_recent_schedule called with team_id=%s, mlbam_team_id=%s", team_id, mlbam_team_id)

    if mlbam_team_id is None:
        return JsonResponse({'error': 'Team not found'}, status=404)

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
