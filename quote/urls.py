from django.urls import path
from .views import QuoteDetailView, QuoteCreateView, QuoteDeleteView
from . import views

urlpatterns = [
    path('', views.view_quotes, name='view-quotes'),
    path('new-quote', QuoteCreateView.as_view(), name='new-quote'),
    path('quote-details/<str:obj_id>', QuoteDetailView.as_view(), name='quote-details'),
    path('delete-quote/<obj_id>', QuoteDeleteView.as_view(), name='quote-delete'),
]

