from django.test import SimpleTestCase
from django.urls import resolve
from user.views import UserDetailView, UserUpdateView
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):
    
    def test_profile_details_url_is_resolved(self):
        resolver = resolve('/user/profile/')
        self.assertEqual(resolver.func.__name__, UserDetailView.as_view().__name__)
    
    def test_update_update_url_is_resolved(self):
        resolver = resolve('/user/profile-update/')
        self.assertEqual(resolver.func.__name__, UserUpdateView.as_view().__name__)
    
    def test_login_url_is_resolved(self):
        resolver = resolve('/login/')
        self.assertEqual(resolver.func.__name__, auth_views.LoginView.as_view().__name__)
    
    def test_logout_url_is_resolved(self):
        resolver = resolve('/logout/')
        self.assertEqual(resolver.func.__name__, auth_views.LogoutView.as_view().__name__)
    
    def test_password_reset_url_is_resolved(self):
        resolver = resolve('/password-reset/')
        self.assertEqual(resolver.func.__name__, auth_views.PasswordResetView.as_view().__name__)
    
    def test_password_reset_done_url_is_resolved(self):
        resolver = resolve('/password-reset/done/')
        self.assertEqual(resolver.func.__name__, auth_views.PasswordResetDoneView.as_view().__name__)
    
    def test_password_reset_done_url_is_resolved(self):
        resolver = resolve('/password-reset-confirm/1/2/')
        self.assertEqual(resolver.func.__name__, auth_views.PasswordResetConfirmView.as_view().__name__)
    
    def test_password_reset_done_url_is_resolved(self):
        resolver = resolve('/password-reset-complete/')
        self.assertEqual(resolver.func.__name__, auth_views.PasswordResetCompleteView.as_view().__name__)
    