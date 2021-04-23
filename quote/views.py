from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from quote.models import Quote, QuoteForm
from quote.services import get_all_quotes, get_single_quote, create_job_with_quote
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from user.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from job.models import Job
from django.core.exceptions import ValidationError

@login_required
def view_quotes(request):
    quotes = get_all_quotes()

    #replace _id with id becasue leading underscore cannot be accessed
    for item in quotes:
        item['id'] = item.pop('_id')
    
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'quote/view_quotes.html', {'page_obj': page_obj})

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
    