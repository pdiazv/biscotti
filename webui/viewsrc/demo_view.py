from django.views.generic import TemplateView, View
from demo import sample_data
from repository import context


class LoadDataView(TemplateView):
    template_name = 'loader.html'

    def get_context_data(self, **kwargs):
        source = sample_data.source
        result = context.DemoContext().parse_sample_data(source)
        
        return {
            'control': { 
                'signup': '', 
                'login': 'active',
                'home': 'hidden',
                'groups': 'hidden',
                'stats': 'hidden',
                'trackers': 'hidden',
                'user': {
                    'name': 'Admin User',
                    'group': 'Admin group'
                }
            },
            'result': result
        }


class StatsTemplateView(TemplateView):
    template_name = 'stats.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.session['user_id']
        user = context.UserContext().get_user(long(user_id))

        return {
            'control': {
                'stats': 'active',
                'signup': 'hidden', 
                'login': 'hidden',
                'user': {
                    'name': user.name,
                    'group': user.group,
                    'picture': user.picture,
                    'points': user.points
                }
            }
        }

import random
from django.http import HttpResponse
from business import feed
from datetime import datetime, timedelta
class StatsDataView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        type = request.GET.get('type')
        group = request.GET.get('group')
        data = []
        nimbbleFeed = feed.ActivityFeed()
        goal = [950,1000,1050,1120,1165,1250,1300][random.randint(0, 6)]

        if type == 'group':
            goal = [520,550,575,580,600,620][random.randint(0, 5)]
            data = nimbbleFeed.activities_by_group(group, 800, 'stats')
        elif type == 'user':
            goal = [120,125,130,140,155,160][random.randint(0,5)]
            user = context.UserContext().get_user(long(group))
            data = nimbbleFeed.activities_by_user(user.key, 800, 'stats')
        else:
            today = datetime.now()
            last_month = today - timedelta(days=30)
            data = nimbbleFeed.recent(
                namespace='stats',
                starting_date= last_month.strftime('%m/%d/%Y'),
                end_date=today.strftime('%m/%d/%Y'),
                limit=800)


        return HttpResponse(json.dumps({
            'info': self.get_info(goal),
            'values': data
        }, cls=DateTimeEncoder), content_type="application/json")


    def get_info(self, goal):
        today = datetime.now()
        last_month = today - timedelta(days=30)

        return {
            'start_date': last_month.strftime('%Y-%m-%dT00:00:00'), #'2015-07-01T00:00:00',
            'end_date': today.strftime('%Y-%m-%dT00:00:00'),
            'goal': goal,
        }

    def get_data(self):
        return [
            { 'datetime': '2014-11-01T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-11-02T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-11-03T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-11-04T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-11-15T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-11-26T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-11-29T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
        ]

import json
import decimal

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       elif isinstance(obj, decimal.Decimal):
           return float(obj)
       else:
           return json.JSONEncoder.default(self, obj)