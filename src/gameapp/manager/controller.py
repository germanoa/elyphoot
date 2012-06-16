from gameapp.models import Manager

def create_manager(nickname, uid):
    if nickname is None or len(nickname) <= 0 or uid < 0:
        return None
        
    manager = Manager(nickname=nickname, uid=uid)
    manager.save()
    
    return manager

def get_manager(request):
    if request is None or\
       request.user is None or\
       not request.user.is_authenticated():
        return None
    
    try:
        manager = Manager.objects.filter(uid=request.user.pk)
    except Manager.DoesNotExist:
        manager = None
    
    return manager