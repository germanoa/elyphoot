from gameapp.models import Manager

def create_manager(nickname, uid):
    if nickname is None or len(nickname) <= 0 or uid < 0:
        return None
        
    manager = Manager(nickname=nickname, uid=uid)
    manager.save()
    
    return manager