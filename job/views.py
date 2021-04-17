from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView
from job.models import Job, JobForm
from job.services import get_all_jobs, get_single_job
from django.db.models import Q

class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'job/view_jobs.html'

    paginate_by = 10

    def get_queryset(self):
        jobs = get_all_jobs()
        q = self.request.GET.get("search", None)

        #if user enters search term
        if q is not None:
            jobs = jobs.filter(
                Q(customer_first_name__icontains=q) |
                Q(customer_last_name__icontains=q) |
                Q(address__icontains=q) |
                Q(customer_phone_num__icontains=q)
                )

        for item in jobs:
            item.id = item._id
        
        return jobs


class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job

    def get_object(self, queryset=None):
        job = get_single_job(self.kwargs.get('obj_id'))
        job.id = job._id

        return job


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    pk_url_kwarg = 'obj_id'

    def get_object(self, queryset=None):
        job = get_single_job(self.kwargs.get('obj_id'))
        job.id = job._id
        return job

    def form_valid(self, form):
        return super().form_valid(form)