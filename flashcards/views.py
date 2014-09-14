from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

class LandingPage(TemplateView):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        context['example_value'] = "Example"
        return context