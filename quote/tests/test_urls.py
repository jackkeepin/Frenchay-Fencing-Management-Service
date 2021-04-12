from django.test import SimpleTestCase
from django.urls import reverse, resolve
from quote.views import home, new_quote, view_quotes, QuoteCreateView, QuoteDetailView

class TestUrls(SimpleTestCase):


    def test_new_quote_url(self):
        resolver = resolve('/quote/new-quote')
        self.assertEqual(resolver.func.view_class, QuoteCreateView)

    
    def test_view_quotes_url_is_resolved(self):
        url = reverse('view-quotes')
        self.assertEqual(resolve(url).func, view_quotes)