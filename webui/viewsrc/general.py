from business.services import SyncService
from django.views.generic import TemplateView, View
from demo import sample_data

class NimbbleTemplateView(TemplateView):

    DefaultPicture = '/static/images/128.png'

    def get_user(self):
        if 'user_id' not in self.request.session:
            return None

        user_id = self.request.session['user_id']
        return context.UserContext().get_user(user_id)

    def get_user_control(self, user):
        return {
            'name': user.name,
            'group': user.group,
            'points': user.points,
            'picture': user.picture if user.picture is not None else self.DefaultPicture
        }


class DefaultView(NimbbleTemplateView):
    template_name = 'cover.html'

    def dispatch(self, request, *args, **kwargs):

        if not 'user_id' in request.session:
            return redirect('webui:login')

        return super(DefaultView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        user = self.get_user()
        
        return {
            'control': {
                'home': 'active',
                'user': self.get_user_control(user)
            }
        }

from business import manager
class TrackersView(NimbbleTemplateView):
    template_name = 'trackers.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']

        user = context.UserContext().get_user(user_id)
        trackers = manager.TrackerManager().list(user_id)

        return {
            'control': {
                'trackers': 'active', 
                'user': self.get_user_control(user)
            },
            'trackers': trackers,
        }


class SimpleTrackerView(NimbbleTemplateView):
    template_name = 'tracker.html'

    def get_context_data(self, **kwargs):
        name = kwargs['tracker_name']
        user_id = self.request.session['user_id']
        user = context.UserContext().get_user(user_id)
        tracker = manager.TrackerManager().sample_data(name, user_id)

        return {
            'control': {
                'tracker': 'active',
                'user': self.get_user_control(user)
            },
            'athlete_template': 'trackers/{0}_athlete.html'.format(name),
            'data_template': 'trackers/{0}_data.html'.format(name),
            'tracker_name': name,
            'athlete': tracker['athlete'],
            'activities': tracker['activities']
        }

class SyncTrackerView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        SyncService().sync(kwargs['tracker_name'], long(kwargs['user_id']))
        return redirect('webui:trackers')


from business import feed
from django.shortcuts import redirect

class MainEmployeeView(NimbbleTemplateView):
    template_name = 'main.html'

    def dispatch(self, request, *args, **kwargs):
        if not 'user_id' in request.session:
            return redirect('webui:login')

        return super(MainEmployeeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        recent = feed.ActivityFeed().recent()
        user = self.get_user()
        
        return {
            'control': {
                'home': 'active',
                'user': self.get_user_control(user)
             },
            'group_name': 'All Departments',
            'recent': recent
        }


from repository import context
class MainUserView(NimbbleTemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']
        if 'user_id' in kwargs:
            user_id = kwargs['user_id']
        user = context.UserContext().get_user(long(user_id))
        activities = feed.ActivityFeed().activities_by_user(user.key)

        return {
            'control': {
                'home': 'active',
                'user': self.get_user_control(self.get_user())
             }, 
            'nimbbleUser': user,
            'nimbbleId': user_id,
            'activities': activities
        }

class GroupView(NimbbleTemplateView):
    template_name = 'group.html'

    def get_context_data(self, **kwargs):
        user = self.get_user()
        group = kwargs['group'] if 'group' in kwargs else user.group

        activities = feed.ActivityFeed().activities_by_group(group)

        return {
            'control': {
                'group': 'active',
                'user': self.get_user_control(user)
            },
            'group_name': group,
            'activities': activities
        }