from django.urls import path
from .views import UserDetailView, UserUpdateView

urlpatterns = [
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('profile-update/', UserUpdateView.as_view(), name='edit-profile'),
]