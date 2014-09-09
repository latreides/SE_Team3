from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

class LandingTest(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_landing(self):
        client_obj = Client()
        path = reverse('landing_page')
        response_obj = client_obj.get(path)
        code = response_obj.status_code
        self.assertEqual(code, 200, str(client_obj) + ' returned: ' + str(code) + ' expected: 200')

