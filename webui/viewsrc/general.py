from business.services import SyncService
from django.views.generic import TemplateView, View
from demo import sample_data

class DefaultView(TemplateView):
    template_name = 'cover.html'

    def get_context_data(self, **kwargs):

        user = { 'name': 'sample user' }

        if 'user_id' not in self.request.session:
            user = context.UserContext().get_random_user()

            if user is None:
                data = sample_data.source
                context.DemoContext().parse_sample_data(data)
                user = context.UserContext().get_random_user()

            self.request.session['user_id'] = user.key.id()
        else:
            user_id = self.request.session['user_id']
            user = context.UserContext().get_user(user_id)
        
        return {
            'control': { 
                'login': 'hidden',
                'signup': 'hidden',
                'home': 'active',
                'user': {'name': user.name, 'group': user.group, 'points': user.points }
            }
        }

from business import manager
class TrackersView(TemplateView):
    template_name = 'trackers.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']
        user = context.UserContext().get_user(user_id)
        trackers = manager.TrackerManager().list(user_id)

        return {
            'control': { 
                'login': 'hidden',
                'signup': 'hidden',
                'trackers': 'active', 
                'user': {
                    'name': user.name, 
                    'group': user.group,
                    'points': user.points
                }
            },
            'trackers': trackers,
        }


class SimpleTrackerView(TemplateView):
    template_name = 'tracker.html'

    def get_context_data(self, **kwargs):
        name = kwargs['tracker_name']
        user_id = self.request.session['user_id']
        user = context.UserContext().get_user(user_id)
        tracker = manager.TrackerManager().sample_data(name, user_id)

        return {
            'control': { 
                'login': 'hidden',
                'signup': 'hidden',
                'tracker': 'active',
                'user': {
                    'name': user.name,
                    'group': user.group,
                    'points': user.points
                }
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

class MainEmployeeView(TemplateView):
    template_name = 'main.html'

    def dispatch(self, request, *args, **kwargs):

        if not 'user_id' in request.session:
            return redirect('webui:login')

        return super(MainEmployeeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        recent = feed.ActivityFeed().recent()
        user_id = self.request.session['user_id']

        user = context.UserContext().get_user(user_id)
        
        return {
            'control': {
                'home': 'active',
                'user': {
                    'name': user.name,
                    'group': user.group,
                    'points': user.points,
                }
             },
            'group_name': 'All Departments',
            'recent': recent
        }


from repository import context
class MainUserView(TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']
        session_user = context.UserContext().get_user(long(user_id))
        if 'user_id' in kwargs:
            user_id = kwargs['user_id']
        user = context.UserContext().get_user(long(user_id))
        activities = feed.ActivityFeed().activities_by_user(user.key)

        return {
            'control': { 
                'login': 'hidden',
                'signup': 'hidden',
                'home': 'active',
                'user': {
                    'name': session_user.name,
                    'group': session_user.group,
                    'points': session_user.points
                }
             }, 
            'nimbbleUser': user,
            'nimbbleId': user_id,
            'activities': activities
        }

class GroupView(TemplateView):
    template_name = 'group.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']
        user = context.UserContext().get_user(long(user_id))
        group = user.group
        if 'group' in kwargs:
            group = kwargs['group']
        activities = feed.ActivityFeed().activities_by_group(group)

        return {
            'control': { 
                'login': 'hidden',
                'signup': 'hidden',
                'group': 'active',
                'user': {
                    'name': user.name,
                    'group': user.group,
                    'points': user.points
                }
            },
            'group_name': group,
            'activities': activities
        }