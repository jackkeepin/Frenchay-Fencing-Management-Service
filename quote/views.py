from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from quote.models import Quote, QuoteForm
from quote.services import get_all_quotes, get_single_quote, create_job_with_quote, create_pdf
from job.services import get_single_job
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from user.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from job.models import Job
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMessage
from smtplib import SMTPException
import os


@csrf_exempt
def create_job(request):
    if request.is_ajax():
        quote_id = request.POST.get('data')
        quote = get_single_quote(quote_id)

        job = create_job_with_quote(quote)

        try:
            job.full_clean()
            job.save()
            quote.associated_job = job._id
            quote.save()

            url = reverse('job-details', kwargs={'obj_id':job._id})
            data = {'success': url}
            return JsonResponse(data)

        except ValidationError as err:
            data = {'error': err.message_dict}
            return JsonResponse(data)
            

@csrf_exempt
def send_quote(request):
    if request.is_ajax():
        quote_id = request.POST.get('data')
        quote = get_single_quote(quote_id)

        try:
            if quote.customer_email == None:
                raise ValidationError('Must have a customer email')
            elif quote.date_of_job == None:
                raise ValidationError('Must have a date of job')
            elif quote.materials == None:
                raise ValidationError('Must have materials')
            elif quote.price_of_materials == None:
                raise ValidationError('Must have price of materials')
            elif quote.price_of_labour == None:
                raise ValidationError('Must have price of labour')
            elif quote.quote_price == None:
                raise ValidationError('Must have quote price')

        except ValidationError as err:
            return JsonResponse( {'status': 'error'} )

        quote.issued_by_first_name = quote.issued_by.first_name
        quote.issued_by_last_name = quote.issued_by.last_name
        quote.issued_by_address = quote.issued_by.address
        quote.issued_by_number = quote.issued_by.phone_num
        quote_dict = vars(quote)

        pdf = create_pdf(quote_dict)

        email = EmailMessage(
            subject='Frenchay Fencing Quote',
            body='Please find attached your quote.',
            from_email=os.environ.get('EMAIL_USER'),
            to=[quote.customer_email]
        )
        email.attach('quote.pdf', pdf, 'application/pdf')
        try:
            email.send()
            quote.sent_quote = True
            quote.save()
            return JsonResponse( {'status': 'success'} )
        except SMTPException as err:
            return JsonResponse( {'status': 'error'} )


class QuoteListView(LoginRequiredMixin, ListView):
    model = Quote
    template_name = "quote/view_quotes.html"
    paginate_by = 10
    

    def get_queryset(self):
        quotes = get_all_quotes()
        q = self.request.GET.get("search", None)

        #if user enters search term
        if q is not None:
            quotes = quotes.filter(
                Q(customer_first_name__icontains=q) |
                Q(customer_last_name__icontains=q) |
                Q(address__icontains=q) |
                Q(customer_phone_num__icontains=q)
                )

        for item in quotes:
            item.id = item._id
        
        return quotes


class QuoteDetailView(LoginRequiredMixin, DetailView):
    model = Quote

    def get_object(self, queryset=None):
        quote = get_single_quote(self.kwargs.get('obj_id'))
        quote.id = quote._id
        return quote
    
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


class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = Quote
    form_class = QuoteForm

    def form_valid(self, form):
        form.instance.issued_by = self.request.user
        form.instance.address = form.cleaned_data['address']

        return super().form_valid(form)


class QuoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    pk_url_kwarg = 'obj_id'

    def get_object(self, queryset=None):
        quote = get_single_quote(self.kwargs.get('obj_id'))
        quote.id = quote._id
        return quote
    
    def get_initial(self):
        quote = get_single_quote(self.kwargs.get('obj_id'))
        quote = vars(quote)
        address = quote['address']
        split_address = address.split(',')
        quote['street'] = split_address[0].lstrip()
        quote['city'] = split_address[1].lstrip()
        quote['post_code'] = split_address[2].lstrip()
        return quote

    def form_valid(self, form):
        form.instance.address = form.cleaned_data['address']
        return super().form_valid(form)


class QuoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Quote
    pk_url_kwarg = 'obj_id'
    success_url = reverse_lazy('view-quotes')
    
    def get_object(self, queryset=None):
        quote = get_single_quote(self.kwargs.get('obj_id'))
        quote.id = quote._id
        
        return quote
    
    def delete(self, request, *args, **kwargs):
        quote = get_single_quote(self.kwargs.get('obj_id'))

        # when quote is deleted also delete associated job
        if quote.associated_job != None:
            job = get_single_job(quote.associated_job)
            job.delete()

        quote.delete()

        success_url = reverse_lazy('view-quotes')
        return HttpResponseRedirect(success_url)
    