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
import yaml
from django.core.files.base import ContentFile

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
        context['most_recent_deck'] = getMostRecentDeck(1)
        context['cards_for_deck'] = getCardsForDeck(1)
        context['last_time_logged_in'] = getLastTimeLoggedIn(1)

        return context


class ScoresPage(LoginRedirect):
    template_name = 'scores_page.html'

    def get_context_data(self, **kwargs):
        context = super(ScoresPage, self).get_context_data(**kwargs)
        context['cardsNotStudied'] = getCountCardsNotStudied(1)
        context['mostRecentDeck'] = getMostRecentDeck(1)
        context['cardsRankedOne'] = getCountCardsWithDifficulty(1, 1)
        context['cardsRankedTwo'] = getCountCardsWithDifficulty(1, 2)
        context['cardsRankedThree'] = getCountCardsWithDifficulty(1, 3)
        context['cardsRankedFour'] = getCountCardsWithDifficulty(1, 4)
        context['cardsRankedFive'] = getCountCardsWithDifficulty(1, 5)
        context['cardCount'] = (getCountCardsWithDifficulty(1, 1) + getCountCardsWithDifficulty(1, 2)
                                + getCountCardsWithDifficulty(1, 3) + getCountCardsWithDifficulty(1, 3)
                                + getCountCardsWithDifficulty(1, 4) + getCountCardsWithDifficulty(1, 5)
                                + getCountCardsNotStudied(1))
        return context


class ViewDeckPage(LoginRedirect):
    template_name = 'view_deck_page.html'

    def get_context_data(self, **kwargs):
        context = super(ViewDeckPage, self).get_context_data(**kwargs)
        context['user_decks'] = getDecksForUser_test(self.request.user)
        return context


class AccountPage(LoginRedirect):
    template_name = 'account_page.html'


class ContactPage(LoginRedirect):
    template_name = 'contact_page.html'


class SigninPage(TemplateView):
    template_name = 'signin_page.html'

    def get_context_data(self, **kwargs):
        invalidLogin = "The username and password combination entered does not match any active user"
        invalidSignup = "The Signup credentials are invalid. Make sure your password entries match or select a new username"
        context = super(SigninPage, self).get_context_data(**kwargs)
        if self.request.GET.get('invalid_login', '') == "True":
            context['invalid_login'] = invalidLogin
        else:
            context['invalid_login'] = ''
        if self.request.GET.get('invalid_signup') == "True":
            context['invalid_signup'] = invalidSignup
        else:
            context['invalid_signup'] = ''
        return context        

    def post(self, request, *args, **kwargs):
        if request.POST.get('signin'):
            if self.signIn(request):
                return HttpResponseRedirect(reverse('landing_page'))
            else:
                return HttpResponseRedirect(reverse('signin') + '?invalid_login=True')
        else:
            if self.signUp(request):
                return HttpResponseRedirect(reverse('landing_page'))
            else:
                return HttpResponseRedirect(reverse('signin') + '?invalid_signup=True')

    def signIn(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return True
        else:
            return False

    def signUp(self, request):
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if User.objects.filter(username = username).count() > 0:
            return False

        if password1 == password2:
            newUser = User.objects.create(username=username, is_active=True, is_staff=False, is_superuser=False)
            newUser.set_password(password1)
            newUser.save()
            user = auth.authenticate(username=username, password=password1)
            auth.login(request, user)
            return True

        else:
            return False

class PlayDeckPage(LoginRedirect):
    template_name = 'play_deck_page.html'


class ImportPage(LoginRedirect):
    template_name = 'import_export_page.html'
    def post(self, request, *args, **kwargs):
        decks = parseConfig()
        deck = request.FILES.get('deck')
        #deck is an open file handle now
        if deck != None:
            if decks.importDeck(request, deck):
                t = loader.get_template('import_export_page.html')
                c = RequestContext(request)
                c['user_decks'] = getDecksForUser_test(self.request.user)
                return HttpResponse(t.render(c), status=200)
            else:
                return HttpResponseRedirect(reverse("import_export_page"))
        else:
            exportFile = decks.exportDeck(request, request.POST.get('deck'))
            exportFileName = str(exportFile) + ".yml"
            deckName = Deck.objects.get(pk = request.POST.get('deck'))
            fileToSend = ContentFile(exportFile)
            response = HttpResponse(fileToSend, 'text/plain')
            response['Content-Length'] = fileToSend.size
            response['Content-Disposition'] = 'attachment; filename = Deck.yml'
            return response
            #else:
                #return HttpResponseRedirect(reverse("import_export_page"))


    def get_context_data(self, **kwargs):
        context = super(ImportPage, self).get_context_data(**kwargs)
        context['user_decks'] = getDecksForUser_test(self.request.user)
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
        newDeck = createDeck(self.request.user.id, 'Untitled Deck')
        newCard = createCard(newDeck.id, True, "Front Side", "Back Side", None, None)

        return HttpResponseRedirect(reverse('edit')+ '?deckId=' + str(newDeck.id))

class EditDeckPage(LoginRedirect):
    template_name = 'edit_deck_page.html'

    def get_context_data(self, **kwargs):
        deckId = self.request.GET.get('deckId')
        if deckId:
            context = super(EditDeckPage, self).get_context_data(**kwargs)
            context['deck'] = getDeck(deckId)
            if context['deck']:
                context['cards'] = getCardsForDeck(deckId)
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
