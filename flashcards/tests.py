from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# This is an abstract Standard Test case intended to perform various generic tests on every view
class StandardTest(TestCase):
    path = ''

    @classmethod
    def setUpClass(cls):
        pass

    # Test if we redirect when not logged in
    def test_redirect(self):
        client_obj = Client()
        response_obj = client_obj.get(self.path)
        code = response_obj.status_code

        self.assertEqual(code, 302, str(client_obj) + ' returned: ' + str(code) + ' expected: 302')

    # Test if we are successfull when logged in
    def test_access(self):
        client_obj = Client()
        test_user = User.objects.create(username='test', is_active=True, is_staff=True, is_superuser=True)
        test_user.set_password('pass')
        test_user.save()
        login = client_obj.login(username='test', password='pass')

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

class WelcomeTest(StandardTest):
    path = reverse('welcome')

    # Welcome does not redirect!
    def test_redirect(self):
        pass
