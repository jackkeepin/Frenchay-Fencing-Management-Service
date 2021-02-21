from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='quote-home'),
    path('new-quote', views.new_quote, name='new-quote'),
    path('view-quotes', views.view_quotes, name='view-quotes'),
]

