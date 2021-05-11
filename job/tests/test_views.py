from django.test import TestCase, Client
from django.urls import reverse, resolve
from user.models import User
from job.models import Job
from job.views import JobDetailView, JobDeleteView, JobUpdateView

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(email='test@email.com', first_name='first', last_name='last', phone_num='12345678901', address='Test address, test city, TT11 1TT', password='testpass123')
        self.client.login(email='test@email.com', password='testpass123')

    def test_view_jobs_view(self):
        url = reverse('view-jobs')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/view_jobs.html', 'general/base.html')

    def test_view_jobs_view_logged_out(self):
        self.client.logout()
        url = reverse('view-jobs')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_job_details_view(self):
        url = reverse('job-details', args=[1])

        self.assertEquals(resolve(url).func.view_class, JobDetailView)
    
    def test_job_details_view_logged_out(self):
        self.client.logout()
        url = reverse('job-details', args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
    
    def test_job_update_view(self):
        url = reverse('job-update', args=[1])

        self.assertEquals(resolve(url).func.view_class, JobUpdateView)
    
    def test_job_update_view_logged_out(self):
        self.client.logout()
        url = reverse('job-update', args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
    
    def test_job_delete_view(self):
        url = reverse('job-delete', args=[1])

        self.assertEquals(resolve(url).func.view_class, JobDeleteView)
    
    def test_job_delete_view_logged_out(self):
        self.client.logout()
        url = reverse('job-delete', args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)