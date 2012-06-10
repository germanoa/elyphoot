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

def runround(request):
    #1. quando um campeonato eh criado, ele deve gerar todos rounds deste campeonato
    #2. quando um round eh criado, ele deve gerar todos matches deste round
    #3. para cada match do round, rodar procedimento que segue com map iterator?
    #4. quando um match eh criado, ele possui 2 teams, aqui recebidos em t1 e t2
    t1=Team.objects.filter(name="INTERNACIONAL")
    t2=Team.objects.filter(name="GREMIO")

    #por enquanto usando player; apos usar squad
    t1_squad=Team_Player.objects.filter(team=t1)
    t2_squad=Team_Player.objects.filter(team=t2)

    #aqui irei colocar algoritmo que simula o jogo
    t1gol=0
    t2gol=0
    for i in range(0,len(t1_squad)):
        if t1_squad[i].player.kick > t2_squad[i].player.kick: t1gol=t1gol+1
        if t1_squad[i].player.kick < t2_squad[i].player.kick: t2gol=t2gol+1
    if t1gol > t2gol: q = "t1!"
    if t1gol < t2gol: q = "t2!"
    
 
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
            basemoney = sw["basemoney"] = 1000000
            formation = 8
            t = Team(name=nameteam,finance=basemoney,formation=formation)
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
