from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, View
from django.core.urlresolvers import reverse
from flashcards.db_interactions import *
from django.contrib import auth
from flashcards.decks import *

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
        context['most_recent_deck'] = GetMostRecentDeck(1)
        context['cards_for_deck'] = GetCardsForDeck(1)
        context['last_time_logged_in'] = GetLastTimeLoggedIn(1)

        return context


class ScoresPage(LoginRedirect):
    template_name = 'scores_page.html'


class ViewDeckPage(LoginRedirect):
    template_name = 'view_deck_page.html'

    def get_context_data(self, **kwargs):
        context = super(ViewDeckPage, self).get_context_data(**kwargs)
        context['user_decks'] = GetDecksForUser_test(self.request.user)
        return context


class AccountPage(LoginRedirect):
    template_name = 'account_page.html'


class ContactPage(LoginRedirect):
    template_name = 'contact_page.html'
        
                
class SigninPage(TemplateView):
    template_name = 'signin_page.html'

    def get_context_data(self, **kwargs):
        invalidLogin = "The username and password combination entered does not match any active user"
        context = super(SigninPage, self).get_context_data(**kwargs)
        if self.request.GET.get('invalid_login', '') == "True":
            context['invalid_login'] = invalidLogin
        else:
            context['invalid_login'] = ''

        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('landing_page'))
        else:
            return HttpResponseRedirect(reverse('signin') + '?invalid_login=True')


class PlayDeckPage(LoginRedirect):
    template_name = 'play_deck_page.html'


class ImportPage(LoginRedirect):
    def post(self, request, *args, **kwargs):
        decks = parseConfig()
        deck = request.FILES.get('deck')
        #deck is an open file handle now
        decks.importDeck(request, deck)
        return HttpResponseRedirect(reverse("import_deck"))
    template_name = 'import_export_page.html'


class WelcomePage(TemplateView):
    template_name = 'welcome_page.html'


class DeleteDeckPage(View):
    def post(self, request, *args, **kwargs):
        deck_id = request.POST.get('deck_id')
        return HttpResponseRedirect(reverse("manage_decks"))


class ResetDeckPage(View):
    def post(self, request, *args, **kwargs):
        deck_id = request.POST.get('deck_id')
        return HttpResponseRedirect(reverse("manage_decks"))
