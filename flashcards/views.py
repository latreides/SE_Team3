from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.generic import TemplateView, ListView, CreateView, View
from django.core.urlresolvers import reverse
from flashcards.db_interactions import *
from django.contrib import auth
from flashcards.decks import *
from django.contrib.auth.models import User
import glob
import ntpath
import os

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

    def get_context_data(self, **kwargs):
        context = super(ScoresPage, self).get_context_data(**kwargs)
        context['cardsNotStudied'] = GetCountCardsNotStudied(1)
        context['mostRecentDeck'] = GetMostRecentDeck(1)
        context['cardsRankedOne'] = GetCountCardsWithDifficulty(1, 1)
        context['cardsRankedTwo'] = GetCountCardsWithDifficulty(1, 2)
        context['cardsRankedThree'] = GetCountCardsWithDifficulty(1, 3)
        context['cardsRankedFour'] = GetCountCardsWithDifficulty(1, 4)
        context['cardsRankedFive'] = GetCountCardsWithDifficulty(1, 5)
        context['cardCount'] = (GetCountCardsWithDifficulty(1, 1) + GetCountCardsWithDifficulty(1, 2)
                                + GetCountCardsWithDifficulty(1, 3) + GetCountCardsWithDifficulty(1, 3)
                                + GetCountCardsWithDifficulty(1, 4) + GetCountCardsWithDifficulty(1, 5)
                                + GetCountCardsNotStudied(1))
        return context


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
        invalidPassword = "The passwords that were entered do not match"
        invalidUsername = "The username chosen is invalid. Try another username."
        context = super(SigninPage, self).get_context_data(**kwargs)
        if self.request.GET.get('invalid_login', '') == "True":
            context['invalid_login'] = invalidLogin
        else:
            context['invalid_login'] = ''
        if self.request.GET.get('invalid_password') == "True":
            context['invalid_signup'] = invalidPassword
        elif self.request.GET.get('invalid_user') == "True":
            context['invalid_signup'] = invalidUsername
        else:
            context['invalid_signup'] = ''
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('signin'):
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('landing_page'))
            else:
                return HttpResponseRedirect(reverse('signin') + '?invalid_login=True')
        else:
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            if User.objects.filter(username = username).count() > 0:
                return HttpResponseRedirect(reverse('signin') + '?invalid_user=True')

            if password1 == password2:
                newUser = User.objects.create(username=username, is_active=True, is_staff=False, is_superuser=False)
                newUser.set_password(password1)
                newUser.save()
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)
                return HttpResponseRedirect(reverse('landing_page'))

            else:
                return HttpResponseRedirect(reverse('signin') + '?invalid_password=True')

class PlayDeckPage(LoginRedirect):
    template_name = 'play_deck_page.html'


class ImportPage(LoginRedirect):
    template_name = 'import_export_page.html'
    def post(self, request, *args, **kwargs):
        decks = parseConfig()
        deck = request.FILES.get('deck')
        #deck is an open file handle now
        if decks.importDeck(request, deck):
            t = loader.get_template('import_export_page.html')
            c = RequestContext(request)
            c['user_decks'] = GetDecksForUser_test(self.request.user)
            return HttpResponse(t.render(c), status=200)
        else:
            return HttpResponseRedirect(reverse("import_export_page"))


    def get_context_data(self, **kwargs):
        context = super(ImportPage, self).get_context_data(**kwargs)
        context['user_decks'] = GetDecksForUser_test(self.request.user)
        return context


class WelcomePage(TemplateView):
    template_name = 'welcome_page.html'


class DeleteDeckPage(View):
    def post(self, request, *args, **kwargs):
        deck_id = request.POST.get('deckId')
        return HttpResponseRedirect(reverse("manage_decks"))


class ResetDeckPage(View):
    def post(self, request, *args, **kwargs):
        deck_id = request.POST.get('deckId')
        return HttpResponseRedirect(reverse("manage_decks"))

class CreateDeckPage(View):
    def post(self, request, *args, **kwargs):
        newDeck = CreateDeck(self.request.user.id, 'Untitled Deck')
        newCard = CreateCard(newDeck.id, True, "Front Side", "Back Side", None, None)

        return HttpResponseRedirect(reverse('edit')+ '?deckId=' + str(newDeck.id))

class EditDeckPage(LoginRedirect):
    template_name = 'edit_deck_page.html'

    def get_context_data(self, **kwargs):
        deckId = self.request.GET.get('deckId')
        if deckId:
            context = super(EditDeckPage, self).get_context_data(**kwargs)
            context['deck'] = getDeck(deckId)
            if context['deck']:
                context['cards'] = GetCardsForDeck(deckId)
                #themeImageList = sorted(glob.glob(settings.THEME_ROOT + '*.*'))
                #themePairList = []
                #for theme in themeImageList:
                #    displayName = ntpath.basename(theme)
                #    theme = theme.replace(settings.THEME_ROOT, settings.THEME_URL, 1);
                #    displayName = os.path.splitext(displayName)[0]
                #    displayName = displayName[displayName.find(':')+1:]
                #    themePairList.append([displayName, theme])
                #context['themes'] =  themePairList
                context['themes'] = Deck.THEME_LIST
            return context
        else:
            pass
