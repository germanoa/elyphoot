from models import Season
from datetime import date
    
def create_season(manager):
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