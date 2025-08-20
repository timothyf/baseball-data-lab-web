from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule, name='api-schedule'),
    path('standings/', views.standings, name='api-standings'),
    path('players/', views.player_search, name='api-player-search'),
    path('players/<int:player_id>/headshot/', views.player_headshot, name='api-player-headshot'),
]
