from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='general-home'),
]

