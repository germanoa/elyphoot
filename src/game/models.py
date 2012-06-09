from django.db import models

class Skill(models.Model):
    kick = models.IntegerField(blank=True)
    brave = models.IntegerField(blank=True)
    luck = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)

class Person(models.Model):
    # ORM fields
    name = models.CharField(max_length=100)
    nick = models.CharField(max_length=20)
    birthday = models.DateField()

class Player(Person):
    POSITIONS = (
        (0, u'Goalkeeper'),
        (1, u'Defense'),
        (2, u'Midfield'),
        (3, u'Forward'),
    )
    # ORM fields
    position = models.IntegerField(choices=POSITIONS)
    skill = models.ForeignKey(Skill)

class Manager(Person):
    # ORM fields
    points = models.IntegerField()
    empregado = models.BooleanField() # pra evitar selects grandes,

class Season(models.Model):
    year = models.IntegerField()

class Championship(models.Model):
    # ORM fields
    name = models.CharField(max_length=100)
    season = models.ForeignKey(Season)

class Round(models.Model):
    # ORM fields
    championship = models.ForeignKey(Championship)

class Team(models.Model):
    # ORM fields
    name = models.CharField(max_length=100)
    player = models.ManyToManyField(Player, related_name="player", through="Team_Player")
    manager = models.ManyToManyField(Manager, through="Team_Manager") 
    squad = models.ManyToManyField(Player, related_name="squad", blank=True ) # join table will be created
    
class Team_Player(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    #season = models.ForeignKey(Season, blank=True)
    salary = models.IntegerField(blank=True)    

class Team_Manager(models.Model):
    team = models.ForeignKey(Team)
    manager = models.ForeignKey(Manager)
    #season = models.ForeignKey(Season, blank=True)
    salary = models.IntegerField(blank=True)    
    
class Match(models.Model):
    # ORM fields
    team1 = models.ForeignKey(Team, related_name="team1")
    team2 = models.ForeignKey(Team, related_name="team2")
    team1_goals = models.IntegerField()
    team2_goals = models.IntegerField()
    roundmatch = models.ForeignKey(Round)    
