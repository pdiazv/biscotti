from django.views.generic import TemplateView, View
from demo import sample_data
from repository import context
from django.shortcuts import redirect


class LoadDataView(TemplateView):
    template_name = 'loader.html'

    def get_context_data(self, **kwargs):
        source = sample_data.source
        result = context.DemoContext().parse_sample_data(source)

        return {
            'control': { 'signup': 'active' },
            'result': result
        }


import random
class StatsTemplateView(TemplateView):
    template_name = 'stats.html'

    def get_context_data(self, **kwargs):

        return {'control': {'stats': 'active'}}

from django.http import HttpResponse
class StatsDataView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps({
            'info': self.get_info(),
            'data': self.get_data()
        }), content_type="application/json")


    def get_info(self):
        return {
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
            { 'datetime': '2014-04-01T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-04-02T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-04-03T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-04-04T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-04-05T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-04-06T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
            { 'datetime': '2014-04-07T00:00:00', 'points': random.randint(400, 1500), 'active': random.randint(100, 150) },
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