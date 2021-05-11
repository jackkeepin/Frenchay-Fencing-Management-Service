from django.test import SimpleTestCase
from django.urls import resolve
from job.views import JobListView, JobDetailView, JobUpdateView, JobDeleteView

class TestUrls(SimpleTestCase):
    
    def test_view_jobs_url_is_resolved(self):
        resolver = resolve('/job/')
        self.assertEqual(resolver.func.__name__, JobListView.as_view().__name__)
    
    def test_job_details_url_is_resolved(self):
        resolver = resolve('/job/job-details/123')
        self.assertEqual(resolver.func.__name__, JobDetailView.as_view().__name__)
    
    def test_job_update_url_is_resolved(self):
        resolver = resolve('/job/job-update/123')
        self.assertEqual(resolver.func.__name__, JobUpdateView.as_view().__name__)
    
    def test_job_delete_url_is_resolved(self):
        resolver = resolve('/job/delete-job/123')
        self.assertEqual(resolver.func.__name__, JobDeleteView.as_view().__name__)