from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.generic import TemplateView, ListView, CreateView, View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.urlresolvers import reverse
from flashcards.db_interactions import *
from django.contrib import auth
from flashcards.decks import *
from urllib import quote, unquote
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset, password_reset_confirm
import glob
import ntpath
import os
import yaml
from django.core.files.base import ContentFile
from next import getNextCard  #To be removed
from play import *
import json

def verify_owner(obj, cls, *args, **kwargs):
    deckId = None
    if 'deckId' in kwargs:
        deckId = kwargs['deckId']
    elif obj.request.GET.get('deckId'):
        deckId = obj.request.GET.get('deckId')

    if deckId:
        deck = getDeck(deckId)
        if not deck or obj.request.user != deck.User_ID:
            return HttpResponseRedirect(reverse('invalid_deck'))

    return super(cls, obj).get(obj.request, *args, **kwargs)

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

    def post(self, request, *args, **kwargs):
        #Open deck view page with keyword arguments passed through url
        enteredSearchText = request.POST.get('search')
        try:
            queryString = self.formQueryString(enteredSearchText)
        except Exception as e:
            return HttpResponseRedirect(reverse('landing_page') + '?' + str(e))
        return HttpResponseRedirect(reverse('deck_search_results') + queryString)

    def formQueryString(self, stringOfKeywords):
        keywords = stringOfKeywords.lower().split()
        if len(keywords) > 0:
            queryString = '?keywords='
            for each in keywords:
                queryString = queryString + self.encodeString(each) + '+'
            queryString = queryString[:len(queryString ) - 1]
            return queryString
        else:
            raise Exception("Invalid Search Parameters")

    def encodeString(self, string):
        return quote(string.encode('utf8'), '')


class ScoresPage(LoginRedirect):
    template_name = 'scores_page.html'

    def get(self, request, *args, **kwargs):
        return verify_owner(self, ScoresPage, *args, **kwargs)

    def get_context_data(self, **kwargs):
       context = super(ScoresPage, self).get_context_data(**kwargs)
       deckId = context.get('deckId')
       context['user_decks'] = getDecksForUser(self.request.user)
       if deckId:
           context['cards'] = getCardsForDeck(deckId)
           context['deck'] = getDeck(deckId)
           context['mostRecentDeck'] = getMostRecentDeck(deckId)
           userDeck = context['user_decks'].get(id=deckId)
           context['deckName']  = userDeck.Name
       else:
           context['cardsNotStudied'] = getCountCardsNotStudied(deckId)
           context['mostRecentDeck'] = getMostRecentDeck(deckId)
           context['cardsRankedOne'] = getCountCardsWithDifficulty(deckId, 1)
           context['cardsRankedTwo'] = getCountCardsWithDifficulty(deckId, 2)
           context['cardsRankedThree'] = getCountCardsWithDifficulty(deckId, 3)
           context['cardsRankedFour'] = getCountCardsWithDifficulty(deckId, 4)
           context['cardsRankedFive'] = getCountCardsWithDifficulty(deckId, 5)
           context['cardCount'] = (getCountCardsWithDifficulty(deckId, 1) + getCountCardsWithDifficulty(deckId, 2)
                                   + getCountCardsWithDifficulty(deckId, 3) + getCountCardsWithDifficulty(deckId, 3)
                                   + getCountCardsWithDifficulty(deckId, 4) + getCountCardsWithDifficulty(deckId, 5)
                                   + getCountCardsNotStudied(deckId))
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
        invalidUsername = "The selected username is invalid. Try another username."
        invalidPassword = "The passwords entered do not match."
        context = super(SigninPage, self).get_context_data(**kwargs)
        if self.request.GET.get('invalid_login', '') == "True":
            context['invalid_login'] = invalidLogin
        else:
            context['invalid_login'] = ''
        if self.request.GET.get('invalid_username', '') == "True":
            context['invalid_signup'] = invalidUsername
        else:
            context['invalid_signup'] = ''
        if self.request.GET.get('invalid_password', '') == "True":
            context['invalid_signup'] = invalidPassword
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('signin'):
            try:
                self.signIn(request)
            except Exception as e:
                return HttpResponseRedirect(reverse('signin') + '?' + str(e) + '=True')

            return HttpResponseRedirect(reverse('landing_page'))

        else:
            try:
                self.signUp(request)
            except Exception as e:
                return HttpResponseRedirect(reverse('signin') + '?' + str(e) + '=True')

            return HttpResponseRedirect(reverse('landing_page'))

    def signIn(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
        else:
            raise Exception('invalid_login')

    def signUp(self, request):
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if User.objects.filter(username = username).count() > 0:
            raise Exception('invalid_username')

        if password1 == password2:
            newUser = User.objects.create(username=username, is_active=True, is_staff=False, is_superuser=False)
            newUser.set_password(password1)
            newUser.save()
            user = auth.authenticate(username=username, password=password1)
            auth.login(request, user)

        else:
            raise Exception('invalid_password')

class PlayDeckPage(LoginRedirect):
    template_name = 'play_deck_page.html'

    def get(self, request, *args, **kwargs):
        return verify_owner(self, PlayDeckPage, *args, **kwargs)

    def post(self, request, *args, **kwards):
        #update card
        pass

    def get_context_data(self, **kwargs):
        #deckId = self.request.GET.get('deck')
        deckId = kwargs.get('deckId', None)
        context = super(PlayDeckPage, self).get_context_data(**kwargs)
        userDeck = getDecksForUser(self.request.user).get(id=deckId)

        context['deckId'] = deckId
        context['deckName']  = userDeck.Name
        context['deckTheme'] = userDeck.Theme.replace(' ', '').replace('.png', '')

        if deckId:
            engineObj = engine()
            #print engineObj.toJson()
            engineObj.play(deckId)
            context['deck'] = engineObj
            context['card'] = engineObj.getNextCard()
            return context
            #self.request.session['playObj'].play(int(deckId))
        else:
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
            result, returnedDeck = decks.importDeck(request, deck)
            if result:
                t = loader.get_template('import_export_page.html')
                c = RequestContext(request)
                c['user_decks'] = getDecksForUser(self.request.user)
                if getCardsForDeck(returnedDeck).count() == 0:
                    createCard(returnedDeck.id, False, "", "")
                    return HttpResponseRedirect(reverse("import_notification_page"))
                else:
                    return HttpResponse(t.render(c), status=200)
            else:
                return HttpResponseRedirect(reverse("import_export_page")+'?deckId='+str(deck.id))
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

class importNotificationPage(TemplateView):
    template_name = 'import_notification_page.html'

    #def get_context_data(self, **kwargs):
        #deckId = self.request.GET.get('deckId')
        #context = super(importNotificationPage, self).get_context_data(**kwargs)
        #context['deckId'] = self.request.GET.get('deckId')
        #return context

    def get_context_data(self, **kwargs):
        deckId = self.request.GET.get('deckId')
        if deckId:
            context = super(importNotificationPage, self).get_context_data(**kwargs)
            context['deck'] = getDeck(deckId)
            if context['deck']:
                context['cards'] = getCardsForDeck(deckId)
                context['themes'] = Deck.THEME_LIST
            return context
        else:
            pass


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

    def get(self, request, *args, **kwargs):
        return verify_owner(self, EditDeckPage, *args, **kwargs)

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

    def post(self, request, *args, **kwargs):
        deckId = self.request.POST.get('deckId')
        cardId = self.request.POST.get('cardId')
        if cardId != None:
            newDifficulty = self.request.POST.get('difficulty')
            card = getCard(cardId)
            card.Difficulty = newDifficulty
            card.save()

        deckObject = getDeck(deckId)

        deckModel = engine()
        deckModel.play(deckId)
        card = deckModel.getNextCard()
        print(card)

        # print "Deck " + str(deckId)
        # print "Card " + str(card)
        # print card.Front_Text
        # print card.Back_Text

        cardData = {'frontText': card.Front_Text, 'backText': card.Back_Text};
        return HttpResponse( json.dumps(cardData), content_type="application/jason")

    def drawCard(self, request, deckID):
        card = getNextCard( int(deckID) )
        return HttpResponse(card)

class deckChangesPage(View):

    def post(self, request, *args, **kwargs):
        cardIdList = self.request.POST.get('cardIdList').split(',')

        deckId = self.request.POST.get('deckId')
        deckName = self.request.POST.get('deckName')
        deckTheme = self.request.POST.get('deckTheme')
        deckTags = self.request.POST.get('deckTags')

        deckObject = getDeck(deckId)
        deckObject.Name = deckName
        deckObject.Theme = deckTheme
        deckObject.Tags = deckTags

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

class deckSearchResults(LoginRedirect):
    template_name = 'deck_search_results.html'

    def get_context_data(self, **kwargs):
        context = super(deckSearchResults, self).get_context_data(**kwargs)
        keywordArgs = self.request.GET.get('keywords', '')
        listOfKeywords = keywordArgs.split()
        keywordsDecoded = [unquote(keyword.decode('utf8', '')) for keyword in listOfKeywords]
        context['matching_decks'] = getSetOfPublicDecksMatching(keywordsDecoded)

        return context

class logout(View):

  def get(self, request, *args, **kwargs):
      auth.logout(request)
      return HttpResponseRedirect(reverse('welcome'))

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='registration/password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('signin'))

def reset(request):
    return password_reset(request, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.text',
        post_reset_redirect=reverse('signin'))


class UploadImagePage(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse("Success!")

class invalidDeckPage(LoginRedirect):
    template_name = 'invalid_deck_page.html'
