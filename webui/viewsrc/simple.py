from django.views.generic import TemplateView, View

class SimpleSignupView(TemplateView):
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        return {
            'control': { 'signup': 'active' },
            'label': 'Sign up',
            'auth_label': 'Please sign up'
        }


from repository import context
from django.shortcuts import redirect
class SimpleAddUserView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.POST

        isSignup = 'signUp' in data
        name, email = data['userName'].strip(), data['userEmail'].strip()
        group = data['userGroup'].strip() if 'userGroup' in data else ''

        if name == '' or email == '':
            return redirect('webui:signup')

        user_id = context.UserContext().add_user({
            'name': name,
            'email': email,
            'group': group
        }, isSignup)

        if user_id is None:
            return redirect('webui:signup')

        request.session['user_id'] = user_id
        return redirect('webui:main_employee')



class SimpleAddActivityView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        #data = request.POST
        user_id = request.session['user_id']

        activity = { 'datetime': '12/4/2014', 'type': 'running', 'source': 'strava', 'distance': 14.5, 'points': 5, 'duration': '02:40:23' }
        context.DemoContext().add_activity(user_id, activity)

        return redirect('webui:main_employee')
