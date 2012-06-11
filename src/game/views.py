from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.http import HttpResponse
from models import *
from datetime import date
import random


import os,sys
from random import randint
from string import Template
from datetime import date
from models import Player,Team,Manager
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


def team_power(t,position):
    power=k=d=s=b=l=h=0
    if position == "md":
        for i in range(0,len(t)):
            k = t[i].player.kick * randint(0,1)
            d = t[i].player.dribble * randint(0,3)
            s = t[i].player.strength * randint(0,2)
            b = t[i].player.brave * randint(0,2)
            l = t[i].player.luck * randint(0,1)
            h = t[i].player.health * randint(0,2)
    if position == "df":
        for i in range(0,t.count()):
            k = t[i].player.kick * randint(0,1)
            d = t[i].player.dribble * randint(0,1)
            s = t[i].player.strength * randint(0,3)
            b = t[i].player.brave * randint(0,2)
            l = t[i].player.luck * randint(0,2)
            h = t[i].player.health * randint(0,2)
    if position == "fw":
        for i in range(0,t.count()):
            k = t[i].player.kick * randint(0,3)
            d = t[i].player.dribble * randint(0,2)
            s = t[i].player.strength * randint(0,1)
            b = t[i].player.brave * randint(0,1)
            l = t[i].player.luck * randint(0,2)
            h = t[i].player.health * randint(0,2)
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


    #por enquanto usando team_player; apos usar squad
    #isto tah mto lento. como melhorar?
    t1=Team.objects.filter(name="SPORT")
    t1name=t1[0].name
    t1color1=t1[0].color1
    t1color2=t1[0].color2
    t1color3=t1[0].color3
    t1_gk=Team_Player.objects.filter(team=t1, player__in=p_gk)
    t1_df=Team_Player.objects.filter(team=t1, player__in=p_df)
    t1_md=Team_Player.objects.filter(team=t1, player__in=p_md)
    t1_fw=Team_Player.objects.filter(team=t1, player__in=p_fw)

    t2=Team.objects.filter(name="GREMIO")
    t2name=t2[0].name
    t2color1=t2[0].color1
    t2color2=t2[0].color2
    t2color3=t2[0].color3
    t2_gk=Team_Player.objects.filter(team=t2, player__in=p_gk)
    t2_df=Team_Player.objects.filter(team=t2, player__in=p_df)
    t2_md=Team_Player.objects.filter(team=t2, player__in=p_md)
    t2_fw=Team_Player.objects.filter(team=t2, player__in=p_fw)

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
                MD1_power = team_power(t1_md,"md")
                if debug: relatorio.append("MD1_POWER: "+str(MD1_power))
                MD2_power = team_power(t2_md,"md")
                if debug: relatorio.append("MD2_POWER: "+str(MD2_power))
                if MD1_power > MD2_power:
                    ballpos="FW1"
                if MD2_power > MD1_power:
                    ballpos="FW2"
        if ballpos == "FW1":
            committal = randint(0,100)
            if committal > 90: 
                FW1_power = team_power(t1_fw,"fw")
                if debug: relatorio.append("FW1_POWER: "+str(FW1_power))
                DF2_power = team_power(t2_df,"df")    
                if debug: relatorio.append("DF2_POWER: "+str(DF2_power))
                if FW1_power > DF2_power:
                    t1gol=t1gol+1
            ballpos="MD"
        if ballpos == "FW2":
            if committal > 90: 
                FW2_power = team_power(t2_fw,"fw")
                if debug: relatorio.append("FW2_POWER: "+str(FW2_power))
                DF1_power = team_power(t1_df,"df")    
                if debug: relatorio.append("DF1_POWER: "+str(DF1_power))
                if FW2_power > DF1_power:
                    t2gol=t2gol+1
            ballpos="MD"
        cronometer=cronometer+1
    return render_to_response('round.html',  locals() , context_instance = RequestContext(request))


def loaddb(request):
    fd = open(os.path.join(os.path.dirname(SITE_ROOT), 'db') + '/jogadores2.csv')
    lines = fd.readlines()
    fd.close()

    jogador_dados = Template("""$name;$nick;$d;$m;$y;$country;$wage;$position;$kick;$brave;$luck;$health;$baseteam""")

    baseteam = ""
    nivelteam = 3
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
            t = Team(name=nameteam,finance=basemoney,formation=formation,color1=color1,color2=color2,color3=color3)
            t.save()
        else:
            if nivelteam == 1:
                skill = randint(35,45)
            if nivelteam == 2:
                skill = randint(25,35)
            if nivelteam == 3:
                skill = randint(15,25)
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
            #print jogador_dados.safe_substitute(sw)
    
            p = Player(name=name,nick=nick,birthday=birthday,country=country,wage=wage,position=position,kick=kick,dribble=dribble,strength=strength,brave=brave,luck=luck,health=health)
            p.save()
            m = Team_Player(player=p,team=t,vinculado=True)
            m.save()
    return render_to_response('loaddb.html',  locals() , context_instance = RequestContext(request))    

class FormNewGame(forms.Form):
    name = forms.CharField(max_length=50)
    def creategame(self):
        #primeiro, o usuario joga direto da database original. vamos implementar multiusuario?
        name = self.cleaned_data.get("name")
        manager = Manager(name=name,nick=name,birthday=date.today(),points=0,empregado=True)
        manager.save()

        total_teams = Team.objects.count()
        if total_teams > 0:        
            n = random.randint(1,total_teams)
            team = Team.objects.get(pk=n)
        else:
            #excecao informando que nao existem times criados
            pass
        
        manager_team = Team_Manager.objects.filter(team=team)
        if manager_team.count() == 0:
            mt = Team_Manager(team=team,manager=manager,salary=1000)
            mt.save()
        else: #time jah possuia treinador
            q_mt = list(manager_team)
            q_mt[0].manager.empregado=False
            q_mt[0].manager.save()
            q_mt[0].manager=manager
            q_mt[0].save()
            
        return team

def newgame(request):
    if request.method == 'POST':
        form = FormNewGame(request.POST)
        if form.is_valid():
            team = form.creategame()            
            welcome = 'Welcome Manager to ' + str(team.name) + '!'
    else:
        form = FormNewGame()
    return render_to_response('newgame.html',  locals() , context_instance = RequestContext(request))
