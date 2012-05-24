from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.http import HttpResponse
from models import *
from datetime import date
import random

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
