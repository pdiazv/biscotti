__author__ = 'pdiazv'

from django.views.generic import TemplateView, View
from django.shortcuts import render_to_response, redirect
from django.utils import http

class DefaultView(TemplateView):
    template_name = 'cover.html'

    def get_context_data(self, **kwargs):
        return {'control': { 'home': 'active' } }