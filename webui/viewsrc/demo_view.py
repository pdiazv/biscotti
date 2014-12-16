from django.views.generic import TemplateView, View
from demo import sample_data
from repository import context
from django.shortcuts import redirect


class LoadDataView(TemplateView):
    template_name = 'loader.html'

    def get_context_data(self, **kwargs):
        source = sample_data.source
        result = context.DemoContext().parse_sample_data(source)
        user_id = self.request.session['user_id']
        user = context.UserContext().get_user(long(user_id))
        
        return {
            'control': { 
                'signup': '', 
                'login': 'active',
                'home': 'hidden',
                'groups': 'hidden',
                'stats': 'hidden',
                'trackers': 'hidden',
                'user': {
                    'name': user.name,
                    'group': user.group
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
                    'group': user.group
                }
            }
        }

import random
from django.http import HttpResponse
from business import feed
class StatsDataView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):

        data = feed.ActivityFeed().recent(
            starting_date='11/1/2014',
            end_date='11/30/2014',
            limit=800)


        return HttpResponse(json.dumps({
            'info': self.get_info(),
            'values': data
        }, cls=DateTimeEncoder), content_type="application/json")


    def get_info(self):
        return {
            'start_date': '2014-11-01T00:00:00',
            'end_date': '2014-12-01T00:00:00',
            'points':{
                'label': 'Points',
                'total': '9,375',
                'difference': 5.8,
                'increase': True,
            },
            'time':{
                'label': 'Active Minutes',
                'total': '3h48m',
                'difference': 1.3,
                'increase': True,
            }
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