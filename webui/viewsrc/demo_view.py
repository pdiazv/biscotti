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


