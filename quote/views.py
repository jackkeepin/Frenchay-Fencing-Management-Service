from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from quote.models import Quote, get_all_quotes, get_single_quote, QuoteForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from user.models import User


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
        return super().form_valid(form)


class QuoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    pk_url_kwarg = 'obj_id'

    def get_object(self, queryset=None):
        quote = get_single_quote(self.kwargs.get('obj_id'))
        quote.id = quote._id
        return quote

    def form_valid(self, form):
        return super().form_valid(form)


class QuoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Quote
    pk_url_kwarg = 'obj_id'
    success_url = reverse_lazy('view-quotes')
    
    def get_object(self, queryset=None):
        quote = get_single_quote(self.kwargs.get('obj_id'))
        quote.id = quote._id
        
        return quote
    