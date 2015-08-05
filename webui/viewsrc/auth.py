from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from google.appengine.api import users

class GoogleLoginView(TemplateView):
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        success_url = reverse('webui:main_employee')
        return {
            'control': { 'login': 'active' },
            'auth_url': users.create_login_url(success_url),
            'label': 'Log in',
            'auth_label': 'Please log in'
        }


class GoogleLogoutView(View):

    def get(self, request, *arg, **kwargs):
        request.session['user_id'] = None
        request.session.flush()

        return redirect('webui:login')


from django.shortcuts import redirect
from business.trackers import strava
class StravaTokenExchangeView(View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):

        if 'error' in request.GET:
            return redirect('webui:trackers')

        code = request.GET.get('code', '')
        user_id = request.session['user_id']

        strava.StravaTracker().add_tracker(user_id, code)

        return redirect('webui:trackers')
