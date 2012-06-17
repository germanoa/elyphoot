# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User

import gameapp.manager.controller
import gameapp.season.controller
import gameapp.round.controller

def is_null_or_empty(value):
    return value is None or len(value) <= 0

def index(request):
    # check if the user is already logged in.
    # if not, show login form (and a link to create account).
    # if yes, redirect to season.

    if request.user is None or not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            
            if is_null_or_empty(username) or is_null_or_empty(password):
                error_message = 'Nome de usuário ou senha inválidos!'
            else:
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_authenticated():
                    auth.login(request, user)
                    
                    # redirect to season view
                    return redirect(reverse('game_season'), context_instance=RequestContext(request))
                else:
                    error_message = 'Nome de usuário ou senha inválidos!'
                
        return render_to_response('account/login.html',  locals() , context_instance=RequestContext(request))
    else:
        # redirect to season view
        return redirect(reverse('game_season'), context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    
    return redirect(reverse('index'), context_instance=RequestContext(request))

def create_account(request):
    # test if data was received and create an account.
    # otherwise show the registration form.
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        retyped_password = request.POST.get('repeat_password', '')
        manager_name = request.POST.get('manager_name', '')
        email = request.POST.get('email', '')
        
        if is_null_or_empty(username):
            error_message = "Nome de usuário inválido!"
        elif is_null_or_empty(email):
            error_message = "Email inválido!"
        elif is_null_or_empty(manager_name):
            error_message = "Nome do manager inválido!"
        elif is_null_or_empty(password) or is_null_or_empty(retyped_password):
            error_message = "Senha inválida!"
        elif password != retyped_password:
            error_message = "As senhas digitadas não conferem!"
        else:
            try:
                user = User.objects.create_user(username, email, password)
                manager = gameapp.manager.controller.create_manager(manager_name, user.pk)
                
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_authenticated():
                    auth.login(request, user)
                    
                    # redirect to season view
                    return redirect(reverse('game_season'), context_instance=RequestContext(request))
                else:
                    error_message = 'Nome de usuário ou senha inválidos!'
                    
            except ValueError:
                error_message = "Nome de usuário inválido!!"
            
    return render_to_response('account/create_account.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/')
def create_season(request):
    # check if is it time to create a season.
    # if current season is over or the manager does not have a season yet,
    # create a new one.
    # always redirect to season
    manager = gameapp.manager.controller.get_or_create_manager(request)
    
    if manager.current_season is None or manager.current_season.completed:
        # only create a new season if the current one is completed or if the current manager does not have a season yet!
        gameapp.season.controller.create_season(manager)
    
    return redirect(reverse('game_season'), context_instance=RequestContext(request))

@login_required(login_url='/')
def season(request):
    # check if manager has a season. if not, redirect to create_season
    manager = gameapp.manager.controller.get_or_create_manager(request)
        
    if manager.current_season is None:
        return redirect(reverse('game_create_season'), context_instance=RequestContext(request))
    
    season = manager.current_season
    teams_serie_a = gameapp.season.controller.get_team_table(season, 1)
    teams_serie_b = gameapp.season.controller.get_team_table(season, 2)
    teams_serie_c = gameapp.season.controller.get_team_table(season, 3)
    teams_serie_d = gameapp.season.controller.get_team_table(season, 4)
    my_team = season.my_team
    
    return render_to_response('game/season.html',  locals() , context_instance=RequestContext(request))

@login_required(login_url='/')
def play_round(request):
    manager = gameapp.manager.controller.get_or_create_manager(request)
        
    season = manager.current_season
    if season is None:
        return redirect(reverse('game_create_season'), context_instance=RequestContext(request))
    
    # if current season has no more rounds to be played or is completed, redirect to season view
    game_round = season.current_round
    if season.completed or game_round is None:
        return redirect(reverse('game_season'), context_instance=RequestContext(request))
    
    my_team = season.my_team
    matches_serie_a = gameapp.round.controller.get_matches_for_serie(game_round, 1)
    matches_serie_b = gameapp.round.controller.get_matches_for_serie(game_round, 2)
    matches_serie_c = gameapp.round.controller.get_matches_for_serie(game_round, 3)
    matches_serie_d = gameapp.round.controller.get_matches_for_serie(game_round, 4)
    
    return render_to_response('game/round.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/')
def play_round_step(request):
    # play one step of the round identified by round_id and return
    # the result (team array or matrix by division)
    
    manager = gameapp.manager.controller.get_or_create_manager(request)
        
    season = manager.current_season
    if season is None:
        return HttpResponse('{}')
    
    # if current season has no more rounds to be played or is completed, redirect to season view
    game_round = season.current_round
    if season.completed or game_round is None:
        return HttpResponse('{}')
    
    if gameapp.round.controller.run_round(season, game_round):
        match_data = serializers.serialize('json', game_round.matches.all())
        cronometer = game_round.matches.all()[0].cronometer
        
        return HttpResponse('{"cronometer":' + str(cronometer) + ', "resolved":' + str(game_round.resolved).lower() + ', "matches":' + match_data + '}')
    else:
        return HttpResponse('{}')

@login_required(login_url='/')
def manage_team(request):
    # show the manage team screen
    return HttpResponse('manage team')

@login_required(login_url='/')
def change_players(request):
    # check if both players belong to season.my_team
    # check if one is squad member and the other not
    # check if there are goalkeepers on the transaction, if so, guarantee that both are
    return HttpResponse('change two players in a team')

@login_required(login_url='/')
def change_formation(request):
    # affect season.my_team
    return HttpResponse('change team formation')