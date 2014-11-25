from django.conf import settings
from django.conf.urls import url, patterns
from webui import views

urlpatterns = patterns('webui.views',
    url(r'^$', views.default, name='home'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
