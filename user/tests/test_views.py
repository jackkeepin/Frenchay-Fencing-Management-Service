from user.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
from user.views import UserDetailView, UserUpdateView

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(email='test@email.com', first_name='first', last_name='last', phone_num='12345678901', address='Test address, test city, TT11 1TT', password='testpass123')
        self.client.login(email='test@email.com', password='testpass123')

    def test_user_detail_view(self):
        url = reverse('profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_detail.html')
    
    def test_user_detail_view_logged_out(self):
        self.client.logout()
        url = reverse('profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
    
    def test_user_update_view(self):
        url = reverse('edit-profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_form.html')
    
    def test_user_update_view_logged_out(self):
        self.client.logout()
        url = reverse('edit-profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)