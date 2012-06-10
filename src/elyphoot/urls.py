from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'elyphoot.views.home', name='home'),
    # url(r'^elyphoot/', include('elyphoot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'game.views.newgame'),
    
    # Load initial data to db
    url(r'^loaddb$', 'game.views.loaddb'),

    # Round
    url(r'^round$', 'game.views.runround'),
)
