from django.test import SimpleTestCase
from django.urls import reverse, resolve
from general.views import home, about, contact

class TestUrls(SimpleTestCase):

    def test_general_home_url_is_resolved(self):
        url = reverse('general-home')
        self.assertEqual(resolve(url).func, home)
    
    def test_general_about_url_is_resolved(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func, about)
    
    def test_general_contact_url_is_resolved(self):
        url = reverse('contact')
        self.assertEqual(resolve(url).func, contact)