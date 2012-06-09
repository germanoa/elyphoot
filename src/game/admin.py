from game.models import Player, Team
from django.contrib import admin

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Person Info',  {'fields': ['name', 'nick', 'birthday']}),
        ('Player Info and Skill',  {'fields': ['position', 'kick', 'brave', 'luck', 'health']}),
    ]

admin.site.register(Player, PlayerAdmin)
admin.site.register(Team)