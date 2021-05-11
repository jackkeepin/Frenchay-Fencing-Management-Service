from django.test import TestCase, Client
from django.urls import reverse
from user.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(email='test@email.com', first_name='first', last_name='last', phone_num='12345678901', address='Test address, test city, TT11 1TT', password='testpass123')
        self.client.login(email='test@email.com', password='testpass123')

    def test_home_view(self):
        url = reverse('general-home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/home.html')
    
    def test_home_logged_out_view(self):
        self.client.logout()
        url = reverse('general-home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/home.html')
    
    def test_about_view(self):
        url = reverse('about')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/about.html')
    
    def test_about_logged_out_view(self):
        self.client.logout()
        url = reverse('about')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/about.html')
    
    def test_contact_view(self):
        url = reverse('contact')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/contact.html')
    
    def test_contact_logged_out_view(self):
        self.client.logout()
        url = reverse('contact')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/contact.html')