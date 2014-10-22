from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


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

class ScoresTest(StandardTest):
    path = reverse('scores')

class ViewDecksTest(StandardTest):
    path = reverse('view_decks')

class AccountTest(StandardTest):
    path = reverse('account')

class ContactTest(StandardTest):
    path = reverse('contact')

class ImportTest(StandardTest):
    path = reverse('import_deck')
    myfile = '''
MyDeck1:
    card1:
        - q: 'What is the square root of 25?'
        - a: '5'
    card2:
        - q: 'What would you do for a klondike bar?'
        - a: 'Nothing'
'''
    
    def test_import_bad(self):
        client_obj = Client()
        file_data = {'deck': SimpleUploadedFile('testdeck.yml', self.myfile)}
        resp = client_obj.post(self.path, file_data)
        self.assertEqual(resp.status_code, 302, str(client_obj) + ' returned: ' + str(resp.status_code) + ' expected: 302')

    def test_import(self):
        client_obj = Client()
        test_user = User.objects.create(username='test', is_active=True, is_staff=True, is_superuser=True)
        test_user.set_password('pass')
        test_user.save()
        login = client_obj.login(username='test', password='pass')
        file_data = {'deck': SimpleUploadedFile('testdeck.yml', self.myfile)}
        resp = client_obj.post(self.path, file_data)
        self.assertEqual(resp.status_code, 200, str(client_obj) + ' returned: ' + str(resp.status_code) + ' expected: 200')


       
    
class SigninTest(StandardTest):
    path = reverse('signin')

    # Signin does not redirect!
    def test_redirect(self):
        pass

class PlayDeckTest(StandardTest):
    path = reverse('play_deck', args=('1',))

class WelcomeTest(StandardTest):
    path = reverse('welcome')

    # Welcome does not redirect!
    def test_redirect(self):
        pass
