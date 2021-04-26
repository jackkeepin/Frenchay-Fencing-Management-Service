from django.urls import path
from .views import QuoteDetailView, QuoteCreateView, QuoteUpdateView, QuoteDeleteView, QuoteListView, create_job, send_quote

urlpatterns = [
    path('', QuoteListView.as_view(), name='view-quotes'),
    path('new-quote', QuoteCreateView.as_view(), name='new-quote'),
    path('quote-details/<str:obj_id>', QuoteDetailView.as_view(), name='quote-details'),
    path('quote-update/<str:obj_id>', QuoteUpdateView.as_view(), name='quote-update'),
    path('delete-quote/<obj_id>', QuoteDeleteView.as_view(), name='quote-delete'),
    path('create-job', create_job, name='create-job'),
    path('send-quote', send_quote, name='send-quote')
]

