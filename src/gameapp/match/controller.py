from random import shuffle
from gameapp.models import Match
from random import randint

def create_matches(teams):
    matches = []
    
    matrix=[]
    #hardcode matrix torneio problem para 8 times
    matrix.append([1,2,3,4,5,6,7,8])
    matrix.append([2,-1,4,3,6,5,8,7])
    matrix.append([3,4,-1,-2,7,8,5,6])
    matrix.append([4,-3,-2,-1,8,7,6,5])
    matrix.append([5,6,7,8,-1,-2,-3,-4])
    matrix.append([6,-5,8,7,-2,-1,-4,-3])
    matrix.append([7,8,-5,-6,-3,-4,-1,-2])
    matrix.append([8,-7,-6,-5,-4,-3,-2,-1])

    turno = []
    returno = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            i_t1 = matrix[j][0]
            i_t2 = matrix[j][i]
            if i_t1 == i_t2 or i_t1 < 0 or i_t2 < 0 : continue
            match = Match(team_a=teams[i_t1-1],\
                           team_b=teams[i_t2-1],\
                           resolved=False,\
                           goals_a=0,\
                           goals_b=0,\
                           serie=teams[i].serie,\
                           cronometer=0,\
                           ball_position='MD')
            turno.append(match)
            
            match = Match(team_b=teams[i_t1-1],\
                           team_a=teams[i_t2-1],\
                           resolved=False,\
                           goals_a=0,\
                           goals_b=0,\
                           serie=teams[i].serie,\
                           cronometer=0,\
                           ball_position='MD')
            returno.append(match)
    
    # concats "turno" and "returno"
    turno.extend(returno)
    return turno

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

def assign_goal(match,who):
    if who == 1: team = match.team_a
    else: team = match.team_b
    position = randint(0,9)
    if position <= 1: #gol da zaga
        p = team.players.filter(squad_member=True, base_player__position=1)
    elif position <= 4: #gol do meiocampo
        p = team.players.filter(squad_member=True, base_player__position=2)
    else: #gol dos atacantes
        p = team.players.filter(squad_member=True, base_player__position=3)
    assigned = randint(0,p.count()-1)
    p[assigned].goals += 1
    p[assigned].save()    

    if who == 1: match.last_goal_assigned_a = p[assigned].base_player.name
    else: match.last_goal_assigned_b = p[assigned].base_player.name

    match.save()
            
def run_match(match):
    if match.resolved:
        return False
    
    committal = randint(0,100)
    if match.ball_position == 'MD':
        if committal > 50:
            players_md1 = match.team_a.players.filter(squad_member=True, base_player__position=2)
            players_md2 = match.team_b.players.filter(squad_member=True, base_player__position=2)
            MD1_power = team_power(players_md1, 'MD')
            MD2_power = team_power(players_md2, 'MD')
            if MD1_power > MD2_power: match.ball_position = 'FW1'
            elif MD2_power > MD1_power: match.ball_position = 'FW2'
                
    elif match.ball_position == 'FW1':
        if committal > 50:
            FW1_power = team_power(match.team_a.players.filter(squad_member=True, base_player__position=3), 'FW')
            DF2_power = team_power(match.team_b.players.filter(squad_member=True, base_player__position=1), 'DF')    
            if FW1_power > DF2_power:
                match.goals_a += 1
                assign_goal(match,1)
        match.ball_position = 'MD'

    elif match.ball_position == 'FW2':
        if committal > 60:
            FW2_power = team_power(match.team_b.players.filter(squad_member=True, base_player__position=3), 'FW')
            DF1_power = team_power(match.team_a.players.filter(squad_member=True, base_player__position=1), 'DF')            
            if FW2_power > DF1_power:
                match.goals_b += 1
                assign_goal(match,2)
        match.ball_position = 'MD'
    
    match.cronometer += 1
    
    if match.cronometer >= 90:
        complete_match(match)
    
    match.save()
    return True
