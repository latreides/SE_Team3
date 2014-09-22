from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.core.urlresolvers import reverse

class LoginRedirect(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('welcome'))
        else:
            return super(LoginRedirect, self).dispatch(request, *args, **kwargs)



class LandingPage(LoginRedirect):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        context['last_deck_viewed'] = "This is the last deck!"
        context['last_visited'] = "This is the last time visited!"
        context['views_for_deck'] = "You viewed this deck x times!"

        return context

class ManageDecksPage(LoginRedirect):
    template_name = 'manage_decks_page.html'

class ScoresPage(LoginRedirect):
    template_name = 'scores_page.html'

class ViewDeckPage(LoginRedirect):
    template_name = 'view_deck_page.html'

class AccountPage(LoginRedirect):
    template_name = 'account_page.html'

class ContactPage(LoginRedirect):
    template_name = 'contact_page.html'

class SigninPage(LoginRedirect):
    template_name = 'signin_page.html'

class PlayDeckPage(LoginRedirect):
    template_name = 'play_deck_page.html'

class WelcomePage(TemplateView):
    template_name = 'welcome_page.html'
