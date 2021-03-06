import gameapp.match.controller
import gameapp.season.controller
from gameapp.models import Round

def run_round(season, game_round):
    if game_round is None or game_round.resolved:
        return False
        
    results = map(gameapp.match.controller.run_match, game_round.matches.all())
    
    for r in results:
        if r:
            return True # algum match ainda nao esta resolvido
    
    game_round.resolved = True
    game_round.save()
    
    if season is not None:
        if game_round.round_number >= len(season.rounds.all()):
            season.completed = True
            season.current_round = None
            season.winner = gameapp.season.controller.get_team_table(season, 1)[0]
        else:
            next_round = game_round.round_number + 1
            season.current_round = season.rounds.get(round_number=next_round)
    
        season.save()
    
    return False # todos os matches resolvidos

def get_matches_for_serie(round, serie):
    return round.matches.filter(serie=serie)

def create_rounds(season):
    matches_serie_a = gameapp.match.controller.create_matches(season.teams.filter(serie=1))
    matches_serie_b = gameapp.match.controller.create_matches(season.teams.filter(serie=2))
    matches_serie_c = gameapp.match.controller.create_matches(season.teams.filter(serie=3))
    matches_serie_d = gameapp.match.controller.create_matches(season.teams.filter(serie=4))
    
    game_round = None
    for match_count in range(len(matches_serie_a)):
        if match_count % 4 == 0:
            if game_round is not None:
                game_round.save()
            
            game_round = Round(round_number=((match_count / 4) + 1), \
                           resolved=False)
            game_round.save()
            season.rounds.add(game_round)
        
        game_round.matches.add(matches_serie_a[match_count])
        game_round.matches.add(matches_serie_b[match_count])
        game_round.matches.add(matches_serie_c[match_count])
        game_round.matches.add(matches_serie_d[match_count])
    
    game_round.save()
    
    season.current_round = season.rounds.get(round_number=1)
    season.save()
