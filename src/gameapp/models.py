# coding=utf-8

from django.db import models

PLAYER_POSITION = (
    (0, u'Goalkeeper'),
    (1, u'Defense'),
    (2, u'Midfield'),
    (3, u'Forward'),
)

TEAM_FORMATION = (
    (0, u'3-3-4'),
    (1, u'3-4-3'),
    (2, u'3-5-2'),
    (3, u'3-6-1'),
    (4, u'2-3-5'),
    (5, u'4-2-4'),
    (6, u'4-3-3'),
    (7, u'4-3-2-1'),
    (8, u'4-4-2'),
    (9, u'4-5-1'),
    (10, u'4-6-0'),
    (11, u'5-3-2'),
    (12, u'5-4-1'),
    (13, u'5-5-0'),
    (14, u'4-1-3-2'),
    (15, u'Carrossel'),
)

TEAM_SERIE = (
    (1, u'Série A'),
    (2, u'Série B'),
    (3, u'Série C'),
    (4, u'Série D'),
)

# blank is only used for validations on django's admin tool
# null is intended to be used for nullable fields on the database

class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    money = models.IntegerField(blank=True, default=0)
    team_formation = models.IntegerField(choices=TEAM_FORMATION)
    color1 = models.CharField(max_length=6)
    color2 = models.CharField(max_length=6)
    color3 = models.CharField(max_length=6)
    serie = models.IntegerField(choices=TEAM_SERIE)
    
    def __unicode__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, null=True, blank=True, related_name='players')
    squad_member = models.BooleanField()
    position = models.IntegerField(choices=PLAYER_POSITION)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    birthday = models.DateField()
    country = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField()
    wage = models.IntegerField(blank=True)
    kick = models.IntegerField(blank=True)
    dribble = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    brave = models.IntegerField(blank=True)
    luck = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    
    def __unicode__(self):
        return self.name + ' [' + self.nickname + ']' 


class TeamInstance(models.Model):
    base_team = models.ForeignKey(Team, related_name='team_instances')
    team_formation = models.IntegerField(choices=TEAM_FORMATION)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    money = models.IntegerField(blank=True, default=0)
    serie = models.IntegerField(choices=TEAM_SERIE)
    
    def reset(self):
        self.wins = 0
        self.loses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
    
    def copy_from_team(self, team):
        self.base_team = team
        self.team_formation = team.team_formation
        self.money = team.money
        self.serie = team.serie
        self.reset()
        self.save()
        
        for p in team.players.all():
            new_p = PlayerInstance()
            new_p.copy_from_player(p, self)
            new_p.save()
    
    def copy_from_team_instance(self, team_instance, position):
        self.base_team = team_instance.base_team
        self.team_formation = team_instance.team_formation
        self.money = team_instance.money
        
        self.serie = team_instance.serie
        if position <= 2:
            if team_instance.serie > 1:
                self.serie = team_instance.serie - 1
        elif position >= 7:
            if team_instance.serie < 4:
                self.serie = team_instance.serie + 1
        
        self.reset()

        self.save()
        
        for p in team_instance.players.all():
            new_p = PlayerInstance()
            new_p.copy_from_player_instance(p, self)
            new_p.save()
    
    def __unicode__(self):
        return self.base_team.name

        
class PlayerInstance(models.Model):
    team = models.ForeignKey(TeamInstance, null=True, blank=True, related_name='players')
    base_player = models.ForeignKey(Player, related_name='player_instances')
    squad_member = models.BooleanField()
    wage = models.IntegerField(blank=True)
    kick = models.IntegerField(blank=True)
    dribble = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    brave = models.IntegerField(blank=True)
    luck = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    
    def copy_from_player(self, player, team_instance):
        self.team = team_instance
        self.base_player = player
        self.squad_member = player.squad_member
        self.wage = player.wage
        self.kick = player.kick
        self.dribble = player.dribble
        self.strength = player.strength
        self.brave = player.brave
        self.luck = player.luck
        self.health = player.health
        
    def copy_from_player_instance(self, player_instance, team_instance):
        self.copy_from_player(player_instance.base_player, team_instance)
        self.squad_member = player_instance.squad_member
        self.wage = player_instance.wage
    
    def __unicode__(self):
        return self.base_player.name

    
class Round(models.Model):
    round_number = models.IntegerField(default=1)
    resolved = models.BooleanField(default=False) # was the round completed?
    
    def __unicode__(self):
        return 'DONE? ' + str(self.resolved)

      
class Season(models.Model):
    current_round = models.ForeignKey(Round, null=True, blank=True, related_name='current_season')
    rounds = models.ManyToManyField(Round, null=True, blank=True, related_name='season')
    winner = models.ForeignKey(TeamInstance, blank=True, null=True, related_name='season_winner')
    my_team = models.ForeignKey(TeamInstance, blank=True, null=True, related_name='season_managed_team')
    teams = models.ManyToManyField(TeamInstance, blank=True, null=True, related_name='season_team')
    year = models.IntegerField()
    completed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.year) + ' | COMPLETED? ' + str(self.completed)

  
class Match(models.Model):
    team_a = models.ForeignKey(TeamInstance, null=True, blank=True, related_name='match_team_a')
    team_b = models.ForeignKey(TeamInstance, null=True, blank=True, related_name='match_team_b')
    round = models.ForeignKey(Round, null=True, blank=False, related_name='matches')
    goals_a = models.IntegerField(default=0)
    goals_b = models.IntegerField(default=0)
    resolved = models.BooleanField(default=False) # was the match played already?
    serie = models.IntegerField(choices=TEAM_SERIE)
    cronometer = models.IntegerField(default=0)
    ball_position = models.CharField(max_length=5, default='MD')
    
    def __unicode__(self):
        if self.resolved:
            return self.team_a.base_team.name + ' ' + str(self.goals_a) + ' X ' + str(self.goals_b) + ' ' + self.team_b.base_team.name
        else:
            return self.team_a.base_team.name + ' ? X ? ' + self.team_b.base_team.name + ' [' + self.ball_position + '] [' + str(self.cronometer) + ']'


class Manager(models.Model):
    current_season = models.ForeignKey(Season, null=True, blank=True, related_name='current_managed_by') # if current_season is null we have to create one before the user is able to play
    season = models.ManyToManyField(Season, null=True, blank=True, related_name='manager')
    nickname = models.CharField(max_length=20, default='Manager')
    total_points = models.IntegerField(default=0)
    uid = models.IntegerField(null=False, blank=False) # related to django user pk
    
    def __unicode__(self):
        return self.nickname


class Result:
    def __init__(self,t1name="",t1goals=0,t1color1="",t1color2="",t1color3="",t2name="",t2goals=0,t2color1="",t2color2="",t2color3=""):
        self.t1name = t1name
        self.t1goals = t1goals
        self.t1color1 = t1color1
        self.t1color2 = t1color2
        self.t1color3 = t1color3
        self.t2name = t2name
        self.t2goals = t2goals
        self.t2color1 = t2color1
        self.t2color2 = t2color2
        self.t2color3 = t2color3
    def __unicode__(self):
        string_result = self.t1name + " " + str(self.t1goals) + " x " + str(self.t2goals) + " " + self.t2name
        return string_result