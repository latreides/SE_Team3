from django.conf.urls import patterns, include, url
from flashcards.views import LandingPage

urlpatterns = patterns('',
                        url(r'^$', LandingPage.as_view(), name='landing_page'),
                       )
