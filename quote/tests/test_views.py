from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_quote_home_view(self):
        url = reverse('quote-home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quote/home.html')
    
    def test_new_quote_view(self):
        url = reverse('new-quote')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quote/new_quote.html')

    def test_view_quotes_view(self):
        url = reverse('view-quotes')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quote/view_quotes.html')