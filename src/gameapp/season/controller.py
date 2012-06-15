from gameapp.models import Season, Team, TeamInstance, Match, Round
from datetime import date
from random import randint, shuffle

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
    copy_teams_from_season_aux(season, last_season.teams.filter(serie=1).order_by('points'))
    copy_teams_from_season_aux(season, last_season.teams.filter(serie=2).order_by('points'))
    copy_teams_from_season_aux(season, last_season.teams.filter(serie=3).order_by('points'))
    copy_teams_from_season_aux(season, last_season.teams.filter(serie=4).order_by('points'))

def copy_teams_from_base(season):
    for t in Team.objects.all():
        ti = TeamInstance()
        ti.copy_from_team(t)
        ti.save()
        season.teams.add(ti) 

def create_matches(teams):
    matches = []
    
    for i in range(len(teams)):
        for j in range(len(teams)):
            if i == j: continue
            
            match = Match(team_a=teams[i],\
                           team_b=teams[j],\
                           resolved=False,\
                           goals_a=0,\
                           goals_b=0,\
                           serie=teams[i].serie,\
                           cronometer=0,\
                           ball_position='MD')
            matches.append(match)
    
    shuffle(matches)
    return matches         

def create_rounds(season):
    matches_serie_a = create_matches(season.teams.filter(serie=1))
    matches_serie_b = create_matches(season.teams.filter(serie=2))
    matches_serie_c = create_matches(season.teams.filter(serie=3))
    matches_serie_d = create_matches(season.teams.filter(serie=4))
    
    round_count = 1
    match_count = 0
    round = None
    for i in range(len(matches_serie_a)):
        if match_count % 4 == 0:
            if round is not None:
                round.save()
        
            round = Round(round_number=round_count,\
                           resolved=False)
            round.save()
            season.rounds.add(round)
            round_count += 1
        
        round.matches.add(matches_serie_a[match_count])
        round.matches.add(matches_serie_b[match_count])
        round.matches.add(matches_serie_c[match_count])
        round.matches.add(matches_serie_d[match_count])
        
        match_count += 1
    
    round.save()
    
    season.current_round = season.rounds.get(round_number=1)
    season.save()

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
    
    create_rounds(season)
    
    season.save()
    
    manager.season.add(season)
    manager.current_season = season
    manager.save()
         
    return season