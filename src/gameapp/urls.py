from django.conf.urls import patterns, url

urlpatterns = patterns('gameapp',
    url(r'^create_account/', 'views.create_account', name='game_create_account'),
    url(r'^create_season/', 'views.create_season', name='game_create_season'),
    url(r'^season/', 'views.season', name='game_season'),
    url(r'^play_round/', 'views.play_round', name='game_play_round'),
     url(r'^play_round_step/', 'views.play_round_step', name='game_play_round_step'),
    url(r'^manage_team/', 'views.manage_team', name='game_manage_team'),
    url(r'^change_players/', 'views.change_players', name='game_change_players'),
    url(r'^change_formation/', 'views.change_formation', name='game_change_formation'),
)