from django.http import HttpResponse

def CreateManager(request):
    return HttpResponse('Create Manager')
    
def CreateSeason(request, manager_id):
    return HttpResponse('Create Season')


