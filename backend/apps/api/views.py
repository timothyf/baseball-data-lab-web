from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET

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
