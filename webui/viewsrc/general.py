__author__ = 'pdiazv'

from django.views.generic import TemplateView, View
from django.shortcuts import render_to_response, redirect
from django.utils import http

class DefaultView(TemplateView):
    template_name = 'cover.html'

    def get_context_data(self, **kwargs):
        return {'control': { 'home': 'active' } }


from business import manager

class TrackersView(TemplateView):
    template_name = 'trackers.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']

        trackers = manager.TrackerManager().list()
        user_trackers = manager.TrackerManager().user_trackers(user_id)

        return {
            'control': { 'trackers': 'active' },
            'trackers': trackers,
            'user_trackers': user_trackers
        }


from repository import context
class MainEmployeeView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']
        user = context.UserContext().get_user(user_id)

        return {
            'control': { 'home': 'active' },
            'employee': { 'name': user.name }
        }