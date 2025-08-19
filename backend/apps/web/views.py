from datetime import date, datetime
from zoneinfo import ZoneInfo
from django.shortcuts import render

try:
    from baseball_data_lab.apis.unified_data_client import UnifiedDataClient
    _bdl_error = None
except Exception as exc:  # pragma: no cover - handles missing dependency
    UnifiedDataClient = None
    _bdl_error = str(exc)


def home(request):
    """Home page displaying today's MLB schedule."""
    message = "baseball-data-lab library is not installed."
    schedule = None
    if UnifiedDataClient is not None:
        current_time = datetime.now().strftime('%H:%M:%S')
        message = (
            f"Using baseball-data-lab UnifiedDataClient to fetch today's schedule. "
        )
        print(f"[home view] Current time: {current_time}")
        try:
            client = UnifiedDataClient()
            try:
                today = datetime.now(ZoneInfo("America/New_York")).date()
            except Exception:  # Fallback if zoneinfo unavailable
                today = date.today()
            schedule = client.get_schedule_for_date_range(today, today)

            # Attach team logo URLs for home and away teams
            try:
                for day in schedule:
                    for game in day.get("games", []):
                        teams = game.get("teams", {})
                        for side in ("home", "away"):
                            team = teams.get(side, {}).get("team")
                            team_id = team.get("id") if team else None
                            if team_id:
                                try:
                                    team["logo_url"] = client.get_team_spot_url(
                                        team_id, 32
                                    )
                                except Exception:  # pragma: no cover - defensive
                                    team["logo_url"] = None
            except Exception:  # pragma: no cover - defensive
                pass
        except Exception as exc:  # pragma: no cover - defensive
            schedule = [f"Error fetching schedule: {exc}"]
    elif _bdl_error:
        message = f"baseball-data-lab import error: {_bdl_error}"
    context = {
        'message': message,
        'schedule': schedule,
    }
    return render(request, 'web/index.html', context)

def schedule(request):
    return render(request, 'web/schedule.html')

def standings(request):
    return render(request, 'web/standings.html')

def players(request):
    return render(request, 'web/players.html')
