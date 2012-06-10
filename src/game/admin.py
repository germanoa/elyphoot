from game.models import Player, Team, Team_Player
from django.contrib import admin

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Person Info',  {'fields': ['name', 'nick', 'birthday']}),
        ('Additional Info', {'fields': ['country', 'wage']}),
        ('Player Info and Skill',  {'fields': ['position', 'kick', 'dribble', 'strength', 'brave', 'luck', 'health']}),
    ] 

class TeamPlayerInline(admin.TabularInline):
    model = Team_Player
    extra = 1

class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'color1', 'color2']}),
        ('Tactical Info', {'fields': ['formation', 'squad']}),
    ]
    
    inlines = (TeamPlayerInline,)

admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
