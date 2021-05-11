from django.test import SimpleTestCase
from django.urls import resolve
from quote.views import QuoteCreateView, QuoteDetailView, QuoteUpdateView, QuoteDeleteView, QuoteListView

class TestUrls(SimpleTestCase):
    
    def test_view_quotes_url_is_resolved(self):
        resolver = resolve('/quote/')
        self.assertEqual(resolver.func.__name__, QuoteListView.as_view().__name__)
    
    def test_view_quotes_url_is_resolved(self):
        resolver = resolve('/quote/new-quote')
        self.assertEqual(resolver.func.__name__, QuoteCreateView.as_view().__name__)
    
    def test_quote_details_url_is_resolved(self):
        resolver = resolve('/quote/quote-details/123')
        self.assertEqual(resolver.func.__name__, QuoteDetailView.as_view().__name__)
    
    def test_quote_update_url_is_resolved(self):
        resolver = resolve('/quote/quote-update/123')
        self.assertEqual(resolver.func.__name__, QuoteUpdateView.as_view().__name__)
    
    def test_quote_delete_url_is_resolved(self):
        resolver = resolve('/quote/delete-quote/123')
        self.assertEqual(resolver.func.__name__, QuoteDeleteView.as_view().__name__)
    