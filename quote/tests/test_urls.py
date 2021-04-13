from django.test import SimpleTestCase
from django.urls import reverse, resolve
from quote.views import view_quotes, QuoteCreateView, QuoteDetailView

class TestUrls(SimpleTestCase):
    
    def test_view_quotes_url_is_resolved(self):
        url = reverse('view-quotes')
        self.assertEqual(resolve(url).func, view_quotes)