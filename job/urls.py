from django.urls import path
from .views import JobListView, JobDetailView

urlpatterns = [
    path('', JobListView.as_view(), name='view-jobs'),
    path('job-details/<str:obj_id>', JobDetailView.as_view(), name='job-details'),
]