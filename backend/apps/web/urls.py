from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('standings/', views.standings, name='standings'),
    path('teams/', views.teams, name='teams'),
    path('team/<int:mlbam_team_id>/', views.team, name='team'),
    path('players/', views.players, name='players'),
    path('game/<int:game_pk>/', views.game, name='game'),
    path('new-game/<int:game_pk>/', views.new_game, name='new_game')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)