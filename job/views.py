from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from job.models import Job
from job.services import get_all_jobs

# Create your views here.
class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'job/view_jobs.html'

    paginate_by = 10

    def get_queryset(self):
        jobs = get_all_jobs()
        q = self.request.GET.get("search", None)

        #if user enters search term
        if q is not None:
            quotes = quotes.filter(
                Q(customer_first_name__icontains=q) |
                Q(customer_last_name__icontains=q) |
                Q(address__icontains=q) |
                Q(customer_phone_num__icontains=q)
                )

        for item in jobs:
            item.id = item._id
        
        return jobs
