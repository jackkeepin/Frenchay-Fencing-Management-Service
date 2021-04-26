from django.test import SimpleTestCase
from django.urls import reverse, resolve
from quote.views import QuoteCreateView, QuoteDetailView, QuoteListView

class TestUrls(SimpleTestCase):
    
    def test_view_quotes_url_is_resolved(self):
        resolver = resolve('/quote/')
        self.assertEqual(resolver.func.__name__, QuoteListView.as_view().__name__)
    