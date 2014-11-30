from django.conf import settings
from django.conf.urls import url, patterns
from webui import views

urlpatterns = patterns('webui.views',
    url(r'^$', views.default, name='home'),
    url(r'^login/$', views.google_login, name='login'),
    url(r'^signup/$', views.simple_signup, name='signup'),
    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^trackers/$', views.trackers, name='trackers'),
    url(r'^main/$', views.main_employee, name='main_employee'),


    url(r'^sv_auth$', views.strava_auth, name='strava_auth')
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
