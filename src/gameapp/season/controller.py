from gameapp.models import Season, Team, TeamInstance
from datetime import date
from random import randint

import gameapp.round.controller

def get_random_team(season):
    teams = season.teams.filter(serie=4)
    
    return teams[randint(0, len(teams) - 1)]

def get_current_team(season, last_season):
    return season.teams.get(base_team=last_season.my_team.base_team)

def copy_teams_from_season_aux(season, teams):
    position = 1
    for t in teams:
        ti = TeamInstance()
        ti.copy_from_team_instance(t, position)
        ti.save()
        season.teams.add(ti)
        position += 1

def copy_teams_from_season(season, last_season):
    copy_teams_from_season_aux(season, get_team_table(last_season, 1))
    copy_teams_from_season_aux(season, get_team_table(last_season, 2))
    copy_teams_from_season_aux(season, get_team_table(last_season, 3))
    copy_teams_from_season_aux(season, get_team_table(last_season, 4))

def copy_teams_from_base(season):
    for t in Team.objects.all():
        ti = TeamInstance()
        ti.copy_from_team(t)
        ti.save()
        season.teams.add(ti)

def create_season(manager):
    if manager is None:
        return None
    
    season = None
    
    last_season = manager.current_season
    
    if last_season is None:
        season = Season(year=(date.today().year))
        season.save()
        copy_teams_from_base(season)
        season.my_team = get_random_team(season)
    else:
        season = Season(year=(last_season.year + 1))
        season.save()
        copy_teams_from_season(season, last_season)
        season.my_team = get_current_team(season, last_season)
    
    season.save()
    
    gameapp.round.controller.create_rounds(season)
    
    manager.season.add(season)
    manager.current_season = season
    manager.save()
         
    return season

def get_team_table(season, serie):
    if season is None:
        return None
    
    return season.teams.filter(serie=serie).order_by('-points')
    