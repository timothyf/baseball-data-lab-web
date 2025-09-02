"""Team-related API views."""

from datetime import datetime
import logging
import re

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from ..models import TeamIdInfo, Venue
from ..utils import require_unified_client
from ..serializers import TeamSearchResultSerializer, TeamInfoSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    parameters=[OpenApiParameter('q', OpenApiTypes.STR, OpenApiParameter.QUERY)],
    responses=TeamSearchResultSerializer(many=True),
)
@api_view(['GET'])
def team_search(request):
    """Search for teams by name."""
    query = request.GET.get('q', '').strip()
    if not query:
        return Response([])

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
    return Response(results)


@extend_schema(responses=TeamInfoSerializer)
@api_view(['GET'])
def team_info(request, mlbam_team_id: int):
    """Return basic team information."""
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
    from . import UnifiedDataClient as _UnifiedDataClient
    if _UnifiedDataClient is not None:
        try:
            client = _UnifiedDataClient()
            team_data = client.fetch_team(int(mlbam_team_id_value))
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

    return Response(row)


@extend_schema(responses={(200, 'text/plain'): OpenApiTypes.STR})
@api_view(['GET'])
@require_unified_client
def team_logo(request, client, mlbam_team_id: int):
    """Return a team's logo image."""

    mlbam_team_id = str(mlbam_team_id)

    try:
        logo_url = client.get_team_logo_url(int(mlbam_team_id))
        return HttpResponse(logo_url, content_type='text/plain')
    except Exception as exc:  # pragma: no cover - defensive
        return Response({'error': str(exc)}, status=500)


@extend_schema(
    parameters=[OpenApiParameter('season', OpenApiTypes.INT, OpenApiParameter.QUERY)],
    responses=OpenApiTypes.OBJECT,
)
@api_view(['GET'])
@require_unified_client
def team_record(request, client, mlbam_team_id: int):
    """Return a team's record for a given season."""

    if mlbam_team_id is None:
        return Response({'error': 'Team not found'}, status=404)

    season_str = request.GET.get('season')
    if season_str is None:
        season_str = str(datetime.now().year)

    try:
        season = int(season_str)
    except ValueError:
        return Response({'error': 'Invalid season'}, status=400)

    try:
        record = client.get_team_record_for_season(season, int(mlbam_team_id))
        return Response(record)
    except Exception as exc:  # pragma: no cover - defensive
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def team_recent_schedule(request, client, mlbam_team_id: int):
    """Return the previous and next five games for a team."""

    try:
        logger.info("Fetching recent schedule for mlbam_team_id=%s", mlbam_team_id)
        schedule = client.get_recent_schedule_for_team(int(mlbam_team_id))
        return Response(schedule)
    except ValueError as ve:
        logger.error("ValueError in team_recent_schedule: %s", ve)
        return Response({'error': str(ve)}, status=400)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Unexpected error in team_recent_schedule: %s", exc)
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def team_roster(request, client, mlbam_team_id: int):
    """Return the current roster for a team."""

    season = datetime.now().year

    try:
        roster = client.fetch_active_roster(int(mlbam_team_id), year=season)
        return Response(roster)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Unexpected error in team_roster: %s", exc)
        return Response({'error': str(exc)}, status=500)


@extend_schema(responses=OpenApiTypes.OBJECT)
@api_view(['GET'])
@require_unified_client
def team_leaders(request, client, mlbam_team_id: int):
    """Return basic batting and pitching leaders for a team."""
    logger.info("Fetching team leaders for mlbam_team_id=%s", mlbam_team_id)

    team_row = (
        TeamIdInfo.objects.filter(mlbam_team_id=mlbam_team_id)
        .values('abbrev')
        .first()
    )
    if team_row is None:
        return Response({'error': 'Team not found'}, status=404)

    abbrev = team_row.get('abbrev')
    season = datetime.now().year
    logger.info("Using team abbrev=%s for mlbam_team_id=%s", abbrev, mlbam_team_id)
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

    pit = pit_df[pit_df.get('TeamNameAbb') == abbrev]
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
    return Response(leaders)