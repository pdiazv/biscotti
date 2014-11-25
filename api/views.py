from django.views.generic import TemplateView, View
from django.utils import simplejson
from django.http import HttpResponse
import random

class ApiGetView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        gen_data = self.get_data(request.GET)
        json_data = simplejson.dumps(gen_data)
        return HttpResponse(json_data, mimetype='application/json')

    def get_data(self, get_params):
        pass

class ChallengeListView(ApiGetView):

    def get_data(self, get_params):
        return [ {'name': 'Challenge 1'} ]


challenge_list = ChallengeListView.as_view()