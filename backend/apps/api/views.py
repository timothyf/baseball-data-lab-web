from datetime import datetime
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET

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
def team_logo(request, team_id: int):
    """Return a team's logo image."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)

    mlbam_team_id = (
        TeamIdInfo.objects.filter(id=team_id)
        .values_list('mlbam_team_id', flat=True)
        .first()
    )

    if mlbam_team_id is None:
        return JsonResponse({'error': 'Team not found'}, status=404)

    mlbam_team_id = str(mlbam_team_id)

    try:
        client = UnifiedDataClient()
        logo_url = client.get_team_logo_url(int(mlbam_team_id))
        return HttpResponse(logo_url, content_type='text/plain')
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse({'error': str(exc)}, status=500)
