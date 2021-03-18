from django.test import SimpleTestCase
from django.urls import reverse, resolve
from quote.views import home, new_quote, view_quotes

class TestUrls(SimpleTestCase):

    # def test_quote_home_url_is_resolved(self):
    #     url = reverse('quote-home')
    #     self.assertEquals(resolve(url).func, home)


    def test_new_quote_url_is_resolved(self):
        url = reverse('new-quote')
        self.assertEqual(resolve(url).func, new_quote)

    
    def test_view_quotes_url_is_resolved(self):
        url = reverse('view-quotes')
        self.assertEqual(resolve(url).func, view_quotes)