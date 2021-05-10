from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from job.models import Job, JobForm
from job.services import get_all_jobs, get_single_job, create_pdf
from quote.services import get_single_quote
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from smtplib import SMTPException
import os


@csrf_exempt
def send_invoice(request):
    if request.is_ajax():
        job_id = request.POST.get('data')
        job = get_single_job(job_id)

        job.issued_by_first_name = job.issued_by.first_name
        job.issued_by_last_name = job.issued_by.last_name
        job.issued_by_address = job.issued_by.address
        job.issued_by_number = job.issued_by.phone_num
        job_dict = vars(job)

        pdf = create_pdf(job_dict)

        email = EmailMessage(
            subject='Frenchay Fencing Invoice',
            body='Please find attached your invoice.\n\nPlease do not reply to this email. Instead, contact us using the details on your invoice.',
            from_email=os.environ.get('EMAIL_USER'),
            to=[job.customer_email],
            cc=[job.issued_by.email]
        )
        email.attach('invoice.pdf', pdf, 'application/pdf')
        try:
            email.send()
            job.sent_invoice = True
            job.save()
            return JsonResponse( {'status': 'success'} )
        except SMTPException as err:
            return JsonResponse( {'status': 'error'} )



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
        
        address = job.address
        address = address.split(",")
        job.street = address[0].lstrip()
        job.city = address[1].lstrip().lower()
        job.post_code = address[2].lstrip()

        return job
    

    def render_to_response(self, context, **response_kwargs):
        # split the materials into an array to display differently on frontend
        context['object'].materials = context['object'].materials.splitlines()
        
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    pk_url_kwarg = 'obj_id'

    def get_object(self, queryset=None):
        job = get_single_job(self.kwargs.get('obj_id'))
        job.id = job._id
        return job
    
    def get_initial(self):
        job = get_single_job(self.kwargs.get('obj_id'))
        job = vars(job)
        address = job['address']
        split_address = address.split(',')
        job['street'] = split_address[0].lstrip()
        job['city'] = split_address[1].lstrip()
        job['post_code'] = split_address[2].lstrip()
        return job

    def form_valid(self, form):
        form.instance.address = form.cleaned_data['address']
        name = form.cleaned_data['customer_first_name'] +  ' ' + form.cleaned_data['customer_last_name']
        messages.success(self.request, 'Job for ' + name + ' updated')

        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    pk_url_kwarg = 'obj_id'
    success_url = reverse_lazy('view-jobs')
    
    def get_object(self, queryset=None):
        job = get_single_job(self.kwargs.get('obj_id'))
        job.id = job._id
        
        return job
    

    def delete(self, request, *args, **kwargs):
        job = get_single_job(self.kwargs.get('obj_id'))

        # when job is deleted also delete associated quote
        quote = get_single_quote(job.associated_quote)
        quote.delete()

        name = job.customer_first_name +  ' ' + job.customer_last_name

        job.delete()

        success_url = reverse_lazy('view-jobs')
        messages.success(self.request, 'Job and associated quote for ' + name + ' deleted')
        return HttpResponseRedirect(success_url)
    