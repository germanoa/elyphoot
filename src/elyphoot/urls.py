from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('gameapp.urls')),
    url(r'^logout/$', 'gameapp.views.logout'),
    url(r'^$', 'gameapp.views.index', name="index"),
)
