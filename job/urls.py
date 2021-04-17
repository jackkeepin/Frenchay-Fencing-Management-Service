from django.urls import path
from .views import JobListView, JobDetailView, JobUpdateView

urlpatterns = [
    path('', JobListView.as_view(), name='view-jobs'),
    path('job-details/<str:obj_id>', JobDetailView.as_view(), name='job-details'),
    path('quote-update/<str:obj_id>', JobUpdateView.as_view(), name='job-update'),
]