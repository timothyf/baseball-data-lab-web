from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule, name='api-schedule'),
    path('standings/', views.standings, name='api-standings'),
    path('players/', views.player_search, name='api-player-search'),
    path('players/<int:player_id>/headshot/', views.player_headshot, name='api-player-headshot'),
    path('teams/', views.team_search, name='api-team-search'),
    path('teams/<int:team_id>/logo/', views.team_logo, name='api-team-logo'),
]
