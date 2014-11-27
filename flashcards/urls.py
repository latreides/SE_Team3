from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from flashcards.views import *

urlpatterns = patterns('',
                        url(r'^$', LandingPage.as_view(), name='landing_page'),
                        url(r'^invalid$', invalidDeckPage.as_view(), name='invalid_deck'),
                        url(r'^scores/(?P<deckId>\d+)$', ScoresPage.as_view(), name='scores'),
                        url(r'^view/(?P<deck>\d+)$', ViewDeckPage.as_view(), name='view_decks'),
                        url(r'^delete_deck/(?P<deck>\d+)$', DeleteDeckPage.as_view(), name='delete_deck'),
                        url(r'^reset_deck/(?P<deck>\d+)$', ResetDeckPage.as_view(), name='reset_deck'),
                        url(r'^import_deck$', ImportPage.as_view(), name='import_deck'),
                        url(r'^scores$', ScoresPage.as_view(), name='scores'),
                        url(r'^view$', ViewDeckPage.as_view(), name='view_decks'),
                        url(r'^edit$', EditDeckPage.as_view(), name='edit'),
                        url(r'^uploadImage$', UploadImagePage.as_view(), name='upload_image'),
                        url(r'^submit$', deckChangesPage.as_view(), name='deck_changes'),
                        url(r'^create$', createDeckPage.as_view(), name='create'),
                        url(r'^account$', AccountPage.as_view(), name='account'),
                        url(r'^contact$', ContactPage.as_view(), name='contact'),
                        url(r'^signin$', SigninPage.as_view(), name='signin'),
                        url(r'^play/(?P<deckId>\d+)$', PlayDeckPage.as_view(), name='play_deck'),
                        url(r'^welcome$', WelcomePage.as_view(), name='welcome'),
                        url(r'files$', ImportPage.as_view(), name='import_export_page'),
                        url(r'^getNextCard$', GetNextCard.as_view(), name='get_next_card'),
                        url(r'^logout$', logout.as_view(), name='logout'),
                        url(r'^deck_search_results$', deckSearchResults.as_view(), name='deck_search_results'),
                        url(r'^import_notification$', importNotificationPage.as_view(), name = 'import_notification_page'),
                        url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'flashcards.views.reset_confirm', name='password_reset_confirm'),
                        url(r'^reset/$', 'flashcards.views.reset', name='reset'),
                        url(r'^cloneDeck/(?P<deckId>\d+)$', cloneDeck.as_view(), name='clone'),
                        url(r'^viewDeck/(?P<deckId>\d+)$', viewDeck.as_view(), name='view_deck')
                       )
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
