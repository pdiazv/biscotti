from django.views.generic import TemplateView, View
from django.utils import simplejson
from django.http import HttpResponse
import random

class ApiChallengeListView(View):
    def get(self, request, *args, **kwargs):
        challenges = [
            {'fb_id': '3156', 'name': 'my zone name'},
            {'fb_id': '4156', 'name': 'other zone'}
        ]

        data = simplejson.dumps(challenges)
        return HttpResponse(data, mimetype='application/json')

challenge_list = ApiChallengeListView.as_view()

