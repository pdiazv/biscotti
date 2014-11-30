from django.conf.urls import *
from lib.appengine_sessions import views

urlpatterns = patterns('',
    url(r'^clean-up/$', views.session_clean_up, name='session-clean-up'),
)
