from django.views.generic import TemplateView, View
from django.shortcuts import render_to_response, redirect
from django.utils import http

class DefaultView(TemplateView):
    template_name = 'cover.html'

    def get_context_data(self, **kwargs):

        if 'user_id' not in self.request.session:
            user = context.UserContext().get_random_user()
            self.request.session['user_id'] = user.key.id()
        
        return {'control': { 'home': 'active' } }

from business import manager

class TrackersView(TemplateView):
    template_name = 'trackers.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']

        trackers = manager.TrackerManager().list(user_id)

        return {
            'control': { 'trackers': 'active' },
            'trackers': trackers,
        }


class SimpleTrackerView(TemplateView):
    template_name = 'tracker.html'

    def get_context_data(self, **kwargs):
        name = kwargs['tracker_name']
        user_id = self.request.session['user_id']

        tracker = manager.TrackerManager().sample_data(name, user_id)

        return {
            'athlete_template': 'trackers/{0}_athlete.html'.format(name),
            'data_template': 'trackers/{0}_data.html'.format(name),
            'control': { 'tracker': 'active' },
            'tracker_name': name,
            'athlete': tracker['athlete'],
            'activities': tracker['activities']
        }

from business import feed
class MainEmployeeView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):

        recent = feed.ActivityFeed().recent()

        return {
            'control': { 'home': 'active' },
            'recent': recent
        }

from repository import context
class MainUserView(TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']
        if 'user_id' in kwargs:
            user_id = kwargs['user_id']
        user = context.UserContext().get_user(long(user_id))
        activities = feed.ActivityFeed().activities_by_user(user.key)

        return {    
            'nimbbleUser': user,
            'activities': activities
        }
