__author__ = 'pdiazv'

from django.views.generic import TemplateView, View

class SimpleSignupView(TemplateView):
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        return { 'control': { 'signup': 'active' } }



from repository import context
from django.shortcuts import redirect
class SimpleAddUserView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.POST

        user_id = context.UserContext().add_user(
            name=data['userName'],
            email=data['userEmail'],
        )

        request.session['user_id'] = user_id
        return redirect('webui:main_employee')

