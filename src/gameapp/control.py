from models import Manager, Season, Team, Player
import datetime
import os
from random import randint
from datetime import date

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
DB_FILENAME = os.path.join(os.path.dirname(SITE_ROOT), 'db') + '/jogadores2.csv'

def CreateManager(nickname, uid):
    if nickname is None or len(nickname) <= 0 or uid < 0:
        return None
        
    manager = Manager(nickname=nickname, uid=uid)
    manager.save()
    
    return manager
    
def CreateSeason(manager):
    if manager is None:
        return None
    
    season = None
    seasons = manager.season.order_by('year')
    first_season = seasons is None or len(seasons) <= 0
    if first_season:
        season = Season(year=(datetime.date.today().year))
    else:
        season = Season(year=(seasons[len(seasons) - 1].year + 1))
    
    season.save()
    
    manager.season.add(season)
    manager.current_season = season
    manager.save()
                
    return season

def PopulateDB():
    fd = open(DB_FILENAME)
    lines = fd.readlines()
    fd.close()

    baseteam = ""
    nivelteam = 4
    skill = 10
    sw = {}
    t = None
    
    for line in lines:
        f = line.split(';')
        if f[1].strip() == 't':
            baseteam = f[0].strip()
            nivelteam = int(f[3].strip())
            nameteam = sw["nameteam"] = f[0].strip()
            countryteam = sw["countryteam"] = f[2].strip()
            color1 = sw["color1"] = f[4].strip()
            color2 = sw["color2"] = f[5].strip()
            color3 = sw["color3"] = f[6].strip()
            basemoney = sw["basemoney"] = 1000000
            formation = 8
            t = Team(name=nameteam,money=basemoney,team_formation=formation,color1=color1,color2=color2,color3=color3,serie=nivelteam)
            t.save()
        else:
            if nivelteam == 1:
                skill = randint(35,45)
            if nivelteam == 2:
                skill = randint(25,35)
            if nivelteam == 3:
                skill = randint(15,25)
            if nivelteam == 4:
                skill = randint(5,15)
            name = sw["name"] = f[0].strip()
            nick = sw["nick"] = f[0].strip()
            d = sw["d"] = randint(1,28)
            m = sw["m"] = randint(1,12)
            y = sw["y"] = randint(1973,1996)
            birthday = date(y,m,d)
            country = sw["country"] = f[2].strip()
            wage = sw["wage"] = randint(skill,skill+10)*10000
            sw["position"] = f[1].strip()
            position = 0
            if f[1].strip() == 'gk': position = 0
            if f[1].strip() == 'df': position = 1
            if f[1].strip() == 'md': position = 2
            if f[1].strip() == 'av': position = 3
            kick = sw["kick"] = randint(skill-5,skill+5)
            dribble = sw["dribble"] = randint(skill-5,skill+5)
            strength = sw["strength"] = randint(skill-5,skill+5)
            brave = sw["brave"] = randint(0,50)
            luck = sw["luck"] = randint(0,50)
            health = sw["health"] = randint(0,50)
            baseteam = sw["baseteam"] = baseteam
    
            p = Player(name=name,\
                        nickname=nick,\
                        birthday=birthday,\
                        country=country,\
                        wage=wage,\
                        position=position,\
                        kick=kick,\
                        dribble=dribble,\
                        strength=strength,\
                        brave=brave,\
                        luck=luck,\
                        health=health,\
                        squad_member=True,\
                        team=t)
            p.save()