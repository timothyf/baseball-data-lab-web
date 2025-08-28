"""API view imports and miscellaneous endpoints."""

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.urls import URLPattern
import logging
import re
from inspect import signature, Parameter

from .schedule import schedule, game_data, predict_game, standings
from .players import (
    player_search,
    player_headshot,
    player_info,
    player_stats,
    league_leaders,
)
from .teams import (
    team_search,
    team_info,
    team_logo,
    team_record,
    team_recent_schedule,
    team_roster,
    team_leaders,
)

try:
    from baseball_data_lab.apis.unified_data_client import UnifiedDataClient
    _bdl_error = None
except Exception as exc:  # pragma: no cover - handles missing dependency
    UnifiedDataClient = None
    _bdl_error = str(exc)

logger = logging.getLogger(__name__)

__all__ = [
    'schedule',
    'game_data',
    'predict_game',
    'standings',
    'player_search',
    'player_headshot',
    'player_info',
    'player_stats',
    'league_leaders',
    'team_search',
    'team_info',
    'team_logo',
    'team_record',
    'team_recent_schedule',
    'team_roster',
    'team_leaders',
    'list_api_endpoints',
    'news',
    'unified_client_methods',
    'unified_client_call',
]


@require_GET
def list_api_endpoints(request):
    from .. import urls as api_urls
    endpoints = []
    query_params = {
        'api-schedule': ['date'],
        'api-player-search': ['q'],
        'api-team-search': ['q'],
        'api-team-record': ['season'],
    }

    for pattern in api_urls.urlpatterns:
        if isinstance(pattern, URLPattern):
            route = pattern.pattern._route
            display = re.sub(r'<[^:>]+:([^>]+)>', r'{\\1}', route)
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
def unified_client_methods(request):
    """Return a list of ``UnifiedDataClient`` methods and required params."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)
    client = UnifiedDataClient()
    methods = []
    for name in dir(client):
        if name.startswith('_'):
            continue
        attr = getattr(client, name)
        if callable(attr):
            sig = signature(attr)
            params = []
            for p in sig.parameters.values():
                if p.name == 'self':
                    continue
                if p.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY):
                    if p.default is Parameter.empty:
                        params.append(p.name)
                    else:
                        if p.default is None:
                            params.append(f"{p.name}")
                        else:
                            params.append(f"{p.name}={p.default!r}")
            methods.append({'name': name, 'params': params})
    methods.sort(key=lambda m: m['name'])
    return JsonResponse({'methods': methods})


@require_GET
def unified_client_call(request, method_name: str):
    """Invoke a ``UnifiedDataClient`` method with query parameters."""
    if UnifiedDataClient is None:
        return JsonResponse({'error': 'baseball-data-lab library is not installed'}, status=500)
    client = UnifiedDataClient()
    if not hasattr(client, method_name):
        return JsonResponse({'error': 'method not found'}, status=404)
    method = getattr(client, method_name)
    sig = signature(method)
    kwargs = {}
    for p in sig.parameters.values():
        if p.name == 'self' or p.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
            continue
        if p.default is Parameter.empty and p.name not in request.GET:
            return JsonResponse({'error': f'missing required parameter: {p.name}'}, status=400)
        if p.name in request.GET:
            val = request.GET[p.name]
            kwargs[p.name] = int(val) if isinstance(val, str) and val.isdigit() else val
    try:
        result = method(**kwargs)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error calling %s: %s", method_name, exc)
        return JsonResponse({'error': str(exc)}, status=500)
    if isinstance(result, (dict, list)):
        return JsonResponse(result, safe=False)
    if isinstance(result, bytes):
        return HttpResponse(result, content_type='application/octet-stream')
    if isinstance(result, str):
        return HttpResponse(result, content_type='text/plain')
    return JsonResponse({'result': str(result)})
