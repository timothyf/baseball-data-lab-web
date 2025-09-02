from django.urls import path

from .views import (
    list_api_endpoints,
    news,
    unified_client_methods,
    unified_client_call,
)
from .views.schedule import schedule, game_data, predict_game, standings
from .views.players import (
    player_search,
    player_info,
    player_stats,
    player_splits,
    player_headshot,
    league_leaders,
)
from .views.teams import (
    team_search,
    team_info,
    team_logo,
    team_record,
    team_recent_schedule,
    team_roster,
    team_leaders,
)

urlpatterns = [
    path('endpoints/', list_api_endpoints, name='api-endpoints'),
    path('unified/methods/', unified_client_methods, name='api-unified-methods'),
    path('unified/<str:method_name>/', unified_client_call, name='api-unified-call'),
    path('schedule/', schedule, name='api-schedule'),
    path('games/<int:game_pk>/', game_data, name='api-game-data'),
    path('games/<int:game_pk>/prediction/', predict_game, name='api-game-prediction'),
    path('standings/', standings, name='api-standings'),
    path('news/', news, name='api-news'),
    path('players/', player_search, name='api-player-search'),
    path('players/<int:player_id>/', player_info, name='api-player-info'),
    path('players/<int:player_id>/stats/', player_stats, name='api-player-stats'),
    path('players/<int:player_id>/splits/', player_splits, name='api-player-splits'),
    path('player/<int:player_id>/headshot/', player_headshot, name='api-player-headshot'),
    path('teams/', team_search, name='api-team-search'),
    path('teams/<int:mlbam_team_id>/', team_info, name='api-team-info'),
    path('teams/<int:mlbam_team_id>/logo/', team_logo, name='api-team-logo'),
    path('teams/<int:mlbam_team_id>/record/', team_record, name='api-team-record'),
    path('teams/<int:mlbam_team_id>/recent_schedule/', team_recent_schedule, name='api-team-recent-schedule'),
    path('teams/<int:mlbam_team_id>/roster/', team_roster, name='api-team-roster'),
    path('leaders/', league_leaders, name='api-league-leaders'),
    path('teams/<int:mlbam_team_id>/leaders/', team_leaders, name='api-team-leaders'),
]