from django.contrib import admin

from .models import PlayerIdInfo, TeamIdInfo, Venue

admin.site.register(PlayerIdInfo)
admin.site.register(TeamIdInfo)
admin.site.register(Venue)
