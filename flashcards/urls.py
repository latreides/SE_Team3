from django.conf.urls import patterns, include, url
from flashcards.views import *

urlpatterns = patterns('',
                        url(r'^$', LandingPage.as_view(), name='landing_page'),
                        url(r'^manage$', ManageDecksPage.as_view(), name='manage_decks'),
                        url(r'^scores$', ScoresPage.as_view(), name='scores'),
                        url(r'^view$', ViewDeckPage.as_view(), name='view_decks'),
                        url(r'^account$', AccountPage.as_view(), name='account'),
                        url(r'^contact$', ContactPage.as_view(), name='contact'),
                        url(r'^signin$', SigninPage.as_view(), name='signin'),
                        url(r'^play$', PlayDeckPage.as_view(), name='play_deck'),
                        url(r'^welcome$', WelcomePage.as_view(), name='welcome'),
                       )
