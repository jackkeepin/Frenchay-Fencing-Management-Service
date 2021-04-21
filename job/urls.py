from django.urls import path
from .views import JobListView, JobDetailView, JobUpdateView, JobDeleteView, send_invoice

urlpatterns = [
    path('', JobListView.as_view(), name='view-jobs'),
    path('job-details/<str:obj_id>', JobDetailView.as_view(), name='job-details'),
    path('job-update/<str:obj_id>', JobUpdateView.as_view(), name='job-update'),
    path('delete-job/<obj_id>', JobDeleteView.as_view(), name='job-delete'),
    path('send-invoice', send_invoice, name='send-invoice'),
]