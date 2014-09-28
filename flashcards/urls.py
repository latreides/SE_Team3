from django.conf.urls import patterns, include, url
from flashcards.views import *

urlpatterns = patterns('',
                        url(r'^$', LandingPage.as_view(), name='landing_page'),
                        url(r'^manage/(?P<deck>\d+)$', ManageDecksPage.as_view(), name='manage_decks'),
                        url(r'^scores/(?P<deck>\d+)$', ScoresPage.as_view(), name='scores'),
                        url(r'^view/(?P<deck>\d+)$', ViewDeckPage.as_view(), name='view_decks'),
                        url(r'^scores/(?P<deck>\d+)$', ScoresPage.as_view(), name='scores'),
                        url(r'^delete_deck/(?P<deck>\d+)$', DeleteDeckPage.as_view(), name='delete_deck'),
                        url(r'^reset_deck/(?P<deck>\d+)$', ResetDeckPage.as_view(), name='reset_deck'),
                        url(r'^manage$', ManageDecksPage.as_view(), name='manage_decks'),
                        url(r'^scores$', ScoresPage.as_view(), name='scores'),
                        url(r'^view$', ViewDeckPage.as_view(), name='view_decks'),
                        url(r'^account$', AccountPage.as_view(), name='account'),
                        url(r'^contact$', ContactPage.as_view(), name='contact'),
                        url(r'^signin$', SigninPage.as_view(), name='signin'),
                        url(r'^play/(?P<deck>\d+)$', PlayDeckPage.as_view(), name='play_deck'),
                        url(r'^welcome$', WelcomePage.as_view(), name='welcome'),
                        url(r'files$', ImportPage.as_view(), name='import_export_page')
                       )
