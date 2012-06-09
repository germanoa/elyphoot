from game.models import Player
from django.contrib import admin

class PlayerAdmin(admin.ModelAdmin):
    

admin.site.register(Player, PlayerAdmin)