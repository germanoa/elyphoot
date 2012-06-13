from models import Manager, Season
import datetime

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