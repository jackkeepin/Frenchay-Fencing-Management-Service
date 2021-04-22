from django.test import TestCase, Client
from django.urls import reverse
from user.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(email='test@email.com', first_name='first', last_name='last', phone_num='12345678901', address='Test address, test city, TT11 1TT', password='testpass123')
        self.client.login(email='test@email.com', password='testpass123')
    
    def test_new_quote_view(self):
        url = reverse('new-quote')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quote/quote_form.html')
    
    def test_new_quote_view_logged_out(self):
        self.client.logout()
        url = reverse('new-quote')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_view_quotes_view(self):
        url = reverse('view-quotes')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quote/view_quotes.html')

    def test_view_quotes_view_logged_out(self):
        self.client.logout()
        url = reverse('view-quotes')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)