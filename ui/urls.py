from django.conf import settings
from django.conf.urls import url, patterns, include

urlpatterns = patterns('ui.views',
    url(r'^', include('webui.urls', namespace='webui')),
    url(r'^api/', include('api.urls', namespace="api")),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
