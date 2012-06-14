from os import path
from datetime import date
from random import randint
from string import Template

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

from models import Player,Team,Manager,Result


SITE_ROOT = path.dirname(path.realpath(__file__))

# skills relevance
def team_power(p,position):
    power=k=d=s=b=l=h=0
    if position == "md":
        for i in range(0,p.count()):
            k = p[i].kick * randint(0,1)
            d = p[i].dribble * randint(0,3)
            s = p[i].strength * randint(0,2)
            b = p[i].brave * randint(0,2)
            l = p[i].luck * randint(0,1)
            h = p[i].health * randint(0,2)
    if position == "df":
        for i in range(0,p.count()):
            k = p[i].kick * randint(0,1)
            d = p[i].dribble * randint(0,1)
            s = p[i].strength * randint(0,3)
            b = p[i].brave * randint(0,2)
            l = p[i].luck * randint(0,2)
            h = p[i].health * randint(0,2)
    if position == "fw":
        for i in range(0,p.count()):
            k = p[i].kick * randint(0,3)
            d = p[i].dribble * randint(0,2)
            s = p[i].strength * randint(0,1)
            b = p[i].brave * randint(0,1)
            l = p[i].luck * randint(0,2)
            h = p[i].health * randint(0,2)
    power = power + k + d + s + b + l + h 
    return power

def runround(request):

    #queries utilizadas para listar players por posicao. Melhorar isso.
    p_gk=Player.objects.filter(position=0)
    p_df=Player.objects.filter(position=1)
    p_md=Player.objects.filter(position=2)
    p_fw=Player.objects.filter(position=3)

    #1. quando um campeonato eh criado, ele deve gerar todos rounds deste campeonato
    #2. quando um round eh criado, ele deve gerar todos matches deste round
    #3. para cada match do round, rodar procedimento que segue com map iterator?
    #4. quando um match eh criado, ele possui 2 teams, aqui recebidos em t1 e t2

    #matches
    m1 = (p_gk,p_df,p_md,p_fw,"INTERNACIONAL","GREMIO")
    m2 = (p_gk,p_df,p_md,p_fw,"SAO PAULO","SANTOS")
    m3 = (p_gk,p_df,p_md,p_fw,"PALMEIRAS","CORINTHIANS")
    m4 = (p_gk,p_df,p_md,p_fw,"FLAMENGO","VASCO")
    matches=[]
    matches.append(m1)
    matches.append(m2)
    matches.append(m3)
    matches.append(m4)
    #exemplo de round
    result = map(runmatch,matches)
    return render_to_response('round.html',  locals() , context_instance = RequestContext(request))

def runmatch(param):
    p_gk=param[0]
    p_df=param[1]
    p_md=param[2]
    p_fw=param[3]
    t1n=param[4]
    t2n=param[5]
    #por enquanto usando player; apos usar player_instance + squad=True
    #isto tah mto lento. como melhorar?
    t1=Team.objects.filter(name=t1n)
    t1name=t1[0].name
    t1color1=t1[0].color1
    t1color2=t1[0].color2
    t1color3=t1[0].color3
    p1_gk=Player.objects.filter(team=t1, position=0)
    p1_df=Player.objects.filter(team=t1, position=1)
    p1_md=Player.objects.filter(team=t1, position=2)
    p1_fw=Player.objects.filter(team=t1, position=3)

    t2=Team.objects.filter(name=t2n)
    t2name=t2[0].name
    t2color1=t2[0].color1
    t2color2=t2[0].color2
    t2color3=t2[0].color3
    p2_gk=Player.objects.filter(team=t2, position=0)
    p2_df=Player.objects.filter(team=t2, position=1)
    p2_md=Player.objects.filter(team=t2, position=2)
    p2_fw=Player.objects.filter(team=t2, position=3)

    t1gol=0
    t2gol=0
    cronometer = 0 #cada iteracao deste while deve ser printado cronometer,t1gol e t2gol. ajax? 
    ballpos="MD"
    relatorio= []
    debug=False
    while (cronometer < 90):
        if ballpos == "MD":
            committal = randint(0,100)
            if committal > 70:
                MD1_power = team_power(p1_md,"md")
                if debug: relatorio.append("MD1_POWER: "+str(MD1_power))
                MD2_power = team_power(p2_md,"md")
                if debug: relatorio.append("MD2_POWER: "+str(MD2_power))
                if MD1_power > MD2_power:
                    ballpos="FW1"
                if MD2_power > MD1_power:
                    ballpos="FW2"
        if ballpos == "FW1":
            committal = randint(0,100)
            if committal > 90:
                FW1_power = team_power(p1_fw,"fw")
                if debug: relatorio.append("FW1_POWER: "+str(FW1_power))
                DF2_power = team_power(p2_df,"df")
                if debug: relatorio.append("DF2_POWER: "+str(DF2_power))
                if FW1_power > DF2_power:
                    t1gol=t1gol+1
            ballpos="MD"
        if ballpos == "FW2":
            if committal > 90:
                FW2_power = team_power(p2_fw,"fw")
                if debug: relatorio.append("FW2_POWER: "+str(FW2_power))
                DF1_power = team_power(p1_df,"df")
                if debug: relatorio.append("DF1_POWER: "+str(DF1_power))
                if FW2_power > DF1_power:
                    t2gol=t2gol+1
            ballpos="MD"
        cronometer=cronometer+1
    r = Result(t1name=t1name,t1goals=t1gol,t1color1=t1color1,t1color2=t1color2,t1color3=t1color3,t2name=t2name,t2goals=t2gol,t2color1=t2color1,t2color2=t2color2,t2color3=t2color3)
    return r

def loaddb(request):
    fd = open(path.join(path.dirname(SITE_ROOT), 'db') + '/jogadores2.csv')
    lines = fd.readlines()
    fd.close()

    jogador_dados = Template("""$name;$nick;$d;$m;$y;$country;$wage;$position;$kick;$brave;$luck;$health;$baseteam""")

    baseteam = ""
    nivelteam = 4
    skill = 10
    sw = {}
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

            p = Player(team=t,name=name,nickname=nick,birthday=birthday,country=country,wage=wage,position=position,kick=kick,dribble=dribble,strength=strength,brave=brave,luck=luck,health=health,squad_member=False)
            p.save()
    return render_to_response('loaddb.html',  locals() , context_instance = RequestContext(request))



def CreateManager(request):
    return HttpResponse('Create Manager')
    
def CreateSeason(request, manager_id):
    return HttpResponse('Create Season')


