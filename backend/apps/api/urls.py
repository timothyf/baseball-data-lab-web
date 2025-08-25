from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule, name='api-schedule'),
    path('games/<int:game_pk>/', views.game_data, name='api-game-data'),
    path('games/<int:game_pk>/prediction/', views.predict_game, name='api-game-prediction'),
    path('standings/', views.standings, name='api-standings'),
    path('news/', views.news, name='api-news'),
    path('players/', views.player_search, name='api-player-search'),
    path('players/<int:player_id>/', views.player_info, name='api-player-info'),
    path('players/<int:player_id>/stats/', views.player_stats, name='api-player-stats'),
    path('player/<int:player_id>/headshot/', views.player_headshot, name='api-player-headshot'),
    path('teams/', views.team_search, name='api-team-search'),
    path('teams/<int:team_id>/', views.team_info, name='api-team-info'),
    path('teams/<int:team_id>/logo/', views.team_logo, name='api-team-logo'),
    path('teams/<int:mlbam_team_id>/record/', views.team_record, name='api-team-record'),
    path('teams/<int:team_id>/recent_schedule/', views.team_recent_schedule, name='api-team-recent-schedule'),
    path('teams/<int:team_id>/roster/', views.team_roster, name='api-team-roster'),
    path('leaders/', views.league_leaders, name='api-league-leaders'),
    path('teams/<int:team_id>/leaders/', views.team_leaders, name='api-team-leaders'),
]
