from django.urls import path
from .views import QuoteDetailView
from . import views

urlpatterns = [
    path('', views.home, name='quote-home'),
    path('new-quote', views.new_quote, name='new-quote'),
    path('view-quotes', views.view_quotes, name='view-quotes'),
    path('quote-details/<str:obj_id>', QuoteDetailView.as_view(), name='quote-details')
]

