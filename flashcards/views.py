from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.generic import TemplateView, ListView, CreateView, View
from django.views.decorators.csrf import ensure_csrf_cookie
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
from next import getNextCard  #To be removed
from play import *

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
        context['most_recent_deck'] = getMostRecentDeck(self.request.user.id)
        context['cards_for_deck'] = getCardsForDeck(1)
        context['last_time_logged_in'] = getLastTimeLoggedIn(self.request.user.id)

        return context


class ScoresPage(LoginRedirect):
    template_name = 'scores_page.html'

    def get_context_data(self, **kwargs):
        context = super(ScoresPage, self).get_context_data(**kwargs)
        context['user_decks'] = getDecksForUser(self.request.user)
        context['cardsNotStudied'] = getCountCardsNotStudied(1)
        context['mostRecentDeck'] = getMostRecentDeck(self.request.user.id)
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
        context['user_decks'] = getDecksForUser(self.request.user)
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

    @ensure_csrf_cookie
    def post(self, request, *args, **kwards):
        #update card
        pass

    def get_context_data(self, **kwargs):
        #deckId = self.request.GET.get('deck')
        deckId = kwargs.get('deck', None)
        if deckId:
            engineObj = engine()
            #print engineObj.toJson()
            context = super(PlayDeckPage, self).get_context_data(**kwargs)
            context['deck'] = engineObj
            return context
            #self.request.session['playObj'].play(int(deckId))
        else:
            context = super(PlayDeckPage, self).get_context_data(**kwargs)
            engineObj = context['deck']
            context['card'] = engineObj.getNextCard()
            return context


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
                c['user_decks'] = getDecksForUser(self.request.user)
                return HttpResponse(t.render(c), status=200)
            else:
                return HttpResponseRedirect(reverse("import_export_page"))
        else:
            exportFile = decks.exportDeck(request, request.POST.get('deck'))
            deckName = Deck.objects.get(pk = request.POST.get('deck')).Name
            fileToSend = ContentFile(exportFile)
            response = HttpResponse(fileToSend, 'text/plain')
            response['Content-Length'] = fileToSend.size
            response['Content-Disposition'] = 'attachment; filename = ' + deckName + '.yml'
            return response
            #else:
                #return HttpResponseRedirect(reverse("import_export_page"))


    def get_context_data(self, **kwargs):
        context = super(ImportPage, self).get_context_data(**kwargs)
        context['user_decks'] = getDecksForUser(self.request.user)
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

class createDeckPage(View):
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
                context['themes'] = Deck.THEME_LIST
            return context
        else:
            pass

#To be removed
class GetNextCard(View):
    def drawCard(self, request, deckID):
        card = getNextCard( int(deckID) )
        return HttpResponse(card)

class deckChangesPage(View):

    def post(self, request, *args, **kwargs):
        cardIdList = self.request.POST.get('cardIdList').split(',')

        deckId = self.request.POST.get('deckId')
        deckName = self.request.POST.get('deckName')
        deckTheme = self.request.POST.get('deckTheme')

        deckObject = getDeck(deckId)
        deckObject.Name = deckName
        deckObject.Theme = deckTheme

        for cardId in cardIdList:
            frontText = self.request.POST.get('front-%s' % cardId)
            backText = self.request.POST.get('back-%s' % cardId)

            # A Numeric ID means the card exists already,
            # a * before a ID means the card is to be deleted
            # anything else is a new card
            if cardId.isnumeric():
                card = getCard(cardId)
                card.Front_Text = frontText
                card.Back_Text = backText
                card.save()
            elif cardId[0] == '*':
                removeId = cardId[1:]
                deleteCard(removeId)
            else:
                createCard(deckId, True, frontText, backText, None, None)

        deckObject.save()
        return HttpResponseRedirect(reverse('edit')+ '?deckId=' + str(deckId))
