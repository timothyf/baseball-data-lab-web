from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('standings/', views.standings, name='standings'),
    path('teams/', views.teams, name='teams'),
    path('team/<int:mlbam_team_id>/', views.team, name='team'),
    path('players/', views.players, name='players'),
]
