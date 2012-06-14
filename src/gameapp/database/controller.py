import elyphoot.settings
import os

from datetime import date
from gameapp.models import Team, Player
from random import randint

DB_FILENAME = os.path.join(os.path.dirname(elyphoot.settings.SITE_ROOT), 'db') + '/jogadores2.csv'

def populate_db():
    fd = open(DB_FILENAME)
    lines = fd.readlines()
    fd.close()

    team_serie = 4
    skill = 10
    t = None
    
    for line in lines:
        f = line.split(';')
        if f[1].strip() == 't':
            team_name = f[0].strip()
            
            team_serie = int(f[3].strip())

            t, created = Team.objects.get_or_create(name=team_name,\
                      defaults={money=1000000,\
                      country=f[2].strip(),\
                      team_formation=8,\
                      color1=f[4].strip(),\
                      color2=f[5].strip(),\
                      color3=f[6].strip(),\
                      serie=team_serie})
                      
            if not created:
                team_serie=t.serie
        else:
            player_name = f[0].strip()
            
            if team_serie == 1: skill = randint(35,45)
            elif team_serie == 2: skill = randint(25,35)
            elif team_serie == 3: skill = randint(15,25)
            elif team_serie == 4: skill = randint(5,15)

            position_name = f[1].strip()
            position = 0
            if position_name == 'gk': position = 0
            elif position_name == 'df': position = 1
            elif position_name == 'md': position = 2
            elif position_name == 'av': position = 3

            p, created = Player.objects.get_or_create(name=player_name,\
                        defaults={nickname=player_name,\
                        birthday=date(randint(1973,1996), randint(1,12), randint(1,28)),\
                        country=f[2].strip(),\
                        wage=randint(skill,skill+10)*10000,\
                        position=position,\
                        kick=randint(skill-5,skill+5),\
                        dribble=randint(skill-5,skill+5),\
                        strength=randint(skill-5,skill+5),\
                        brave=randint(0,50),\
                        luck=randint(0,50),\
                        health=randint(0,50),\
                        squad_member=True,\
                        team=t})