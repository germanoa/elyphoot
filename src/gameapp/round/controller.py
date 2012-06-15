from random import randint

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
             
def run_match(match):
    if match.resolved:
        return False
    
    if match.cronometer >= 90:
        match.resolved = True
        match.save()
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
    match.save()
    return True