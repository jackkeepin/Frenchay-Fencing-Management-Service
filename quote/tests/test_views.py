from quote.models import Quote
from django.test import TestCase, Client
from django.urls import reverse, resolve
from user.models import User
from quote.views import QuoteListView, QuoteCreateView, QuoteDetailView, QuoteUpdateView, QuoteDeleteView

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(email='test@email.com', first_name='first', last_name='last', phone_num='12345678901', address='Test address, test city, TT11 1TT', password='testpass123')
        self.client.login(email='test@email.com', password='testpass123')
        quote=Quote(customer_first_name="TestFirstName")
        quote.save()
    
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
        
    def test_quote_list_view(self):
        url = reverse('view-quotes')

        self.assertEquals(resolve(url).func.view_class, QuoteListView)
    
    def test_quote_create_view(self):
        url = reverse('new-quote')

        self.assertEquals(resolve(url).func.view_class, QuoteCreateView)
    
    def test_quote_create_view_logged_out(self):
        self.client.logout()
        url = reverse('new-quote')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
    
    def test_quote_detail_view(self):
        url = reverse('quote-details', args=[1])

        self.assertEquals(resolve(url).func.view_class, QuoteDetailView)
    
    def test_quote_detail_view_logged_out(self):
        self.client.logout()
        url = reverse('quote-details', args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
    
    def test_quote_update_view(self):
        url = reverse('quote-update', args=[1])

        self.assertEquals(resolve(url).func.view_class, QuoteUpdateView)
    
    def test_quote_update_view_logged_out(self):
        self.client.logout()
        url = reverse('quote-update', args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
    
    def test_quote_delete_view(self):
        url = reverse('quote-delete', args=[1])

        self.assertEquals(resolve(url).func.view_class, QuoteDeleteView)
    
    def test_quote_delete_view_logged_out(self):
        self.client.logout()
        url = reverse('quote-delete', args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
    
