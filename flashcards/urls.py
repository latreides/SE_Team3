from django.conf.urls import patterns, include, url
from flashcards.views import *

urlpatterns = patterns('',
                        url(r'^$', LandingPage.as_view(), name='landing_page'),
                        url(r'^scores/(?P<deckId>\d+)$', ScoresPage.as_view(), name='scores'),
                        url(r'^view/(?P<deck>\d+)$', ViewDeckPage.as_view(), name='view_decks'),
                        url(r'^delete_deck/(?P<deck>\d+)$', DeleteDeckPage.as_view(), name='delete_deck'),
                        url(r'^reset_deck/(?P<deck>\d+)$', ResetDeckPage.as_view(), name='reset_deck'),
                        url(r'^import_deck$', ImportPage.as_view(), name='import_deck'),
                        url(r'^scores$', ScoresPage.as_view(), name='scores'),
                        url(r'^view$', ViewDeckPage.as_view(), name='view_decks'),
                        url(r'^edit$', EditDeckPage.as_view(), name='edit'),
                        url(r'^submit$', deckChangesPage.as_view(), name='deck_changes'),
                        url(r'^create$', createDeckPage.as_view(), name='create'),
                        url(r'^account$', AccountPage.as_view(), name='account'),
                        url(r'^contact$', ContactPage.as_view(), name='contact'),
                        url(r'^signin$', SigninPage.as_view(), name='signin'),
                        url(r'^play/(?P<deck>\d+)$', PlayDeckPage.as_view(), name='play_deck'),
                        url(r'^welcome$', WelcomePage.as_view(), name='welcome'),
                        url(r'files$', ImportPage.as_view(), name='import_export_page'),
                        url(r'^getNextCard/(?P<deckID>\d+)$', GetNextCard().drawCard, name='get_next_card'),
                        url(r'^logout$', logout.as_view(), name='logout'),
                        url(r'^deck_search_results$', deckSearchResults.as_view(), name='deck_search_results'),
                        url(r'^import_notification$', importNotificationPage.as_view(), name = 'import_notification_page')
                       )
