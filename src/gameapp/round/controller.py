from random import randint
import gameapp.match.controller

def team_power(players, ball_position):
    power = 0
    
    if ball_position == 'MD':
        for p in players:
            k = p.kick * randint(0,1)
            d = p.dribble * randint(0,3)
            s = p.strength * randint(0,2)
            b = p.brave * randint(0,2)
            l = p.luck * randint(0,1)
            h = p.health * randint(0,2)
            power = power + k + d + s + b + l + h
    elif ball_position == 'DF':
        for p in players:
            k = p.kick * randint(0,1)
            d = p.dribble * randint(0,1)
            s = p.strength * randint(0,3)
            b = p.brave * randint(0,2)
            l = p.luck * randint(0,2)
            h = p.health * randint(0,2)
            power = power + k + d + s + b + l + h
    elif ball_position == 'FW':
        for p in players:
            k = p.kick * randint(0,3)
            d = p.dribble * randint(0,2)
            s = p.strength * randint(0,1)
            b = p.brave * randint(0,1)
            l = p.luck * randint(0,2)
            h = p.health * randint(0,2)
            power = power + k + d + s + b + l + h
    
    return power

def complete_match(match):
    match.resolved = True
        
    match.team_a.goals_for += match.goals_a
    match.team_a.goals_against += match.goals_b
        
    match.team_b.goals_for += match.goals_b
    match.team_b.goals_against += match.goals_a
        
    if match.goals_a > match.goals_b:
        match.team_a.wins += 1
        match.team_a.points += 3    
        match.team_b.loses += 1
        
    elif match.goals_b > match.goals_a:
        match.team_b.wins += 1
        match.team_b.points += 3
        match.team_a.loses += 1
        
    else:
        match.team_a.draws += 1
        match.team_a.points += 1    
        match.team_b.draws += 1
        match.team_b.points += 1
        
    match.team_a.save()
    match.team_b.save()
            
def run_match(match):
    if match.resolved:
        return False
    
    committal = randint(0,100)
    if match.ball_position == 'MD':
        if committal > 70:
            MD1_power = team_power(match.team_a.players.filter(squad_member=True, base_player__position=2), 'MD')
            MD2_power = team_power(match.team_b.players.filter(squad_member=True, base_player__position=2), 'MD')  
            if MD1_power > MD2_power: match.ball_position = 'FW1'
            elif MD2_power > MD1_power: match.ball_position = 'FW2'
                
    elif match.ball_position == 'FW1':
        if committal > 90:
            FW1_power = team_power(match.team_a.players.filter(squad_member=True, base_player__position=3), 'FW')
            DF2_power = team_power(match.team_b.players.filter(squad_member=True, base_player__position=1), 'DF')    
            if FW1_power > DF2_power: match.goals_a += 1
        match.ball_position = 'MD'

    elif match.ball_position == 'FW2':
        if committal > 90:
            FW2_power = team_power(match.team_b.players.filter(squad_member=True, base_player__position=3), 'FW')
            DF1_power = team_power(match.team_a.players.filter(squad_member=True, base_player__position=1), 'DF')            
            if FW2_power > DF1_power: match.goals_b += 1
        match.ball_position = 'MD'
    
    match.cronometer += 1
    
    if match.cronometer >= 90:
        complete_match(match)
    
    match.save()
    return True

def run_round(round):
    if round is None or round.resolved:
        return False
        
    results = map(run_match, round.matches.all())
    
    for r in results:
        if r:
            return True # algum match ainda nao esta resolvido
    
    round.resolved = True
    round.save()
    
    # informa 'season' que este round acabou para ir para o 
    # proximo ou encerrar o campeonato
    
    return False # todos os matches resolvidos
    

def create_rounds(season):
    matches_serie_a = gameapp.match.controller.create_matches(season.teams.filter(serie=1))
    matches_serie_b = gameapp.match.controller.create_matches(season.teams.filter(serie=2))
    matches_serie_c = gameapp.match.controller.create_matches(season.teams.filter(serie=3))
    matches_serie_d = gameapp.match.controller.create_matches(season.teams.filter(serie=4))
    
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