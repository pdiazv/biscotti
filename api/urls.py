from django.conf import settings
from django.conf.urls import url, patterns
from api import stubviews
from api import views

urlpatterns = patterns('api.views',
    url(r'^challenge/list$', stubviews.challenge_list, {}, name='challenge-list'),           # get
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
