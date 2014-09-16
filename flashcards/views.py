from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

class LandingPage(TemplateView):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        context['example_value'] = "Example"
        return context

class ManageDecksPage(TemplateView):
    template_name = 'manage_decks_page.html'

class ScoresPage(TemplateView):
    template_name = 'scores_page.html'

class ViewDeckPage(TemplateView):
    template_name = 'view_deck_page.html'

class AccountPage(TemplateView):
    template_name = 'account_page.html'

class ContactPage(TemplateView):
    template_name = 'contact_page.html'

class SigninPage(TemplateView):
    template_name = 'signin_page.html'

class PlayDeckPage(TemplateView):
    template_name = 'play_deck_page.html'
