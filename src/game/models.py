from django.db import models

class Person(models.Model):
    # ORM fields
    name = models.CharField(max_length=100)
    nick = models.CharField(max_length=20)
    birthday = models.DateField()
    
    def __unicode__(self):
        return self.name + ' [' + self.nick + ']'

class Player(Person):
    POSITIONS = (
        (0, u'Goalkeeper'),
        (1, u'Defense'),
        (2, u'Midfield'),
        (3, u'Forward'),
    )
    # ORM fields
    country = models.CharField(max_length=5)
    wage = models.IntegerField(blank=True)
    position = models.IntegerField(choices=POSITIONS)
    kick = models.IntegerField(blank=True)
    dribble = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    brave = models.IntegerField(blank=True)
    luck = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    
    def __unicode__(self):
        return self.name + ' [' + self.nick + ']'

class Manager(Person):
    # ORM fields
    points = models.IntegerField()
    empregado = models.BooleanField() # pra evitar selects grandes,
    
    def __unicode__(self):
        return base.__unicode__()

class Season(models.Model):
    year = models.IntegerField()

class Championship(models.Model):
    # ORM fields
    name = models.CharField(max_length=100)
    season = models.ForeignKey(Season)
    
    def __unicode__(self):
        return self.name

class Round(models.Model):
    # ORM fields
    championship = models.ForeignKey(Championship)

class Team(models.Model):
    FORMATION = (
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
    # ORM fields
    finance = models.IntegerField(blank=True)
    name = models.CharField(max_length=100)
    player = models.ManyToManyField(Player, related_name="player", through="Team_Player")
    formation = models.IntegerField(choices=FORMATION)
    squad = models.ManyToManyField(Player, related_name="squad", blank=True) # join table will be created
    manager = models.ManyToManyField(Manager, through="Team_Manager")
    color1 = models.CharField(max_length=20)
    color2 = models.CharField(max_length=20)
    color3 = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name
    
class Team_Player(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    vinculado = models.BooleanField()    

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
