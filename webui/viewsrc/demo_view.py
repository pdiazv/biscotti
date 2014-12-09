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
class StatsDataView(TemplateView):
    template_name = 'stats.html'

    def get_context_data(self, **kwargs):

        return {
            'control': { 'stats': 'active' },
            'info': self.get_info(),
            'data': self.get_data()
        }


    def get_sample_stats(self):
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
            { 'day_label': 's', 'date': '04/01/2014', 'value': random.randint(400, 1500) },
            { 'day_label': 'm', 'date': '04/02/2014', 'value': random.randint(450, 1400) },
            { 'day_label': 't', 'date': '04/03/2014', 'value': random.randint(420, 1600) },
            { 'day_label': 'w', 'date': '04/04/2014', 'value': random.randint(430, 1200) },
            { 'day_label': 't', 'date': '04/05/2014', 'value': random.randint(440, 1400) },
            { 'day_label': 'f', 'date': '04/06/2014', 'value': random.randint(400, 1530) },
            { 'day_label': 's', 'date': '04/07/2014', 'value': random.randint(400, 1000) },
            { 'day_label': 's', 'date': '04/08/2014', 'value': random.randint(400, 1500) },
            { 'day_label': 'm', 'date': '04/09/2014', 'value': random.randint(450, 1400) },
            { 'day_label': 't', 'date': '04/10/2014', 'value': random.randint(420, 1600) },
            { 'day_label': 'w', 'date': '04/11/2014', 'value': random.randint(430, 1200) },
            { 'day_label': 't', 'date': '04/12/2014', 'value': random.randint(440, 1400) },
            { 'day_label': 'f', 'date': '04/13/2014', 'value': random.randint(400, 1530) },
            { 'day_label': 's', 'date': '04/14/2014', 'value': random.randint(400, 1000) },
        ]