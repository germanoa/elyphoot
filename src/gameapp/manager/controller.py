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
        manager = Manager.objects.get(uid=request.user.pk)
    except Manager.DoesNotExist:
        manager = None
    
    return manager

def get_or_create_manager(request):
    manager = get_manager(request)
    
    if manager is None:
        manager = create_manager(request.user.username, request.user.pk)
    
    return manager