from random import shuffle

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