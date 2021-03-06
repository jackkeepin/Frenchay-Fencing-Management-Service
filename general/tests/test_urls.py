from django.test import SimpleTestCase
from django.urls import reverse, resolve
from general.views import home

class TestUrls(SimpleTestCase):

    def test_general_home_url_is_resolved(self):
        url = reverse('general-home')
        self.assertEqual(resolve(url).func, home)