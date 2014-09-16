from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

class StandardTest(TestCase):
    path = ''

    @classmethod
    def setUpClass(cls):
        pass

    def test_redirect(self):
        pass

    def test_access(self):
        client_obj = Client()
        response_obj = client_obj.get(self.path)
        code = response_obj.status_code
        self.assertEqual(code, 200, str(client_obj) + ' returned: ' + str(code) + ' expected: 200')

class LandingTest(StandardTest):
    path = reverse('landing_page')

class ManageDecksTest(StandardTest):
    path = reverse('manage_decks')

class ScoresTest(StandardTest):
    path = reverse('scores')

class ViewDecksTest(StandardTest):
    path = reverse('view_decks')

class AccountTest(StandardTest):
    path = reverse('account')

class ContactTest(StandardTest):
    path = reverse('contact')

class SigninTest(StandardTest):
    path = reverse('signin')

class PlayDeckTest(StandardTest):
    path = reverse('play_deck')
