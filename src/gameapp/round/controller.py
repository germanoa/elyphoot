import gameapp.match.controller
from gameapp.models import Round

def run_round(game_round):
    if game_round is None or game_round.resolved:
        return False
        
    results = map(gameapp.match.controller.run_match, game_round.matches.all())
    
    for r in results:
        if r:
            return True # algum match ainda nao esta resolvido
    
    game_round.resolved = True
    game_round.save()
    
    if game_round.current_season is not None:
        if game_round.round_number < 14:
            game_round.current_season.completed = True
            game_round.current_season.save()
            game_round.current_season = None
            game_round.save()
        else:
            next_round = game_round.current_season.rounds.get(round_number=(game_round.round_number + 1))
            next_round.current_season = game_round.current_season
            next_round.save()
    
    return False # todos os matches resolvidos
    

def create_rounds(season):
    matches_serie_a = gameapp.match.controller.create_matches(season.teams.filter(serie=1))
    matches_serie_b = gameapp.match.controller.create_matches(season.teams.filter(serie=2))
    matches_serie_c = gameapp.match.controller.create_matches(season.teams.filter(serie=3))
    matches_serie_d = gameapp.match.controller.create_matches(season.teams.filter(serie=4))
    
    round_count = 1
    match_count = 0
    game_round = None
    for i in range(len(matches_serie_a)):
        if match_count % 4 == 0:
            if game_round is not None:
                game_round.save()
        
            game_round = Round(round_number=round_count,\
                           resolved=False)
            game_round.save()
            season.rounds.add(round)
            round_count += 1
        
        game_round.matches.add(matches_serie_a[match_count])
        game_round.matches.add(matches_serie_b[match_count])
        game_round.matches.add(matches_serie_c[match_count])
        game_round.matches.add(matches_serie_d[match_count])
        
        match_count += 1
    
    game_round.save()
    
    season.current_round = season.rounds.get(round_number=1)
    season.save()