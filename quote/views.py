from django.shortcuts import render
from quote.models import Quote, get_all_quotes, get_single_quote, QuoteForm
from django.views.generic import DetailView, CreateView, DeleteView
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy

test_quotes = [
    {
        'quoteId': '123abc',
        'customer': 'bob',
        'cost': '£100'
    },
    {
        'quoteId': '456def',
        'customer': 'alice',
        'cost': '£300'
    }
]

def home(request):
    context = {
        'quotes': test_quotes,
        'title': 'Home'
    }
    return render(request, 'quote/home.html', context)

def new_quote(request):
    return render(request, 'quote/new_quote.html')

def view_quotes(request):
    quotes = get_all_quotes()

    #replace _id with id becasue leading underscore cannot be accessed
    for item in quotes:
        item['id'] = item.pop('_id')
    
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'quote/view_quotes.html', {'page_obj': page_obj})


class QuoteDetailView(DetailView):
    model = Quote

    def get_object(self, queryset=None):
        quote = vars(get_single_quote(self.kwargs.get('obj_id')))
        quote['id'] = quote.pop('_id')
        
        return quote


class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteForm

    def form_valid(self, form):
        return super().form_valid(form)


class QuoteDeleteView(DeleteView):
    model = Quote
    pk_url_kwarg = 'obj_id'
    success_url = reverse_lazy('view-quotes')
    
    def get_object(self, queryset=None):
        quote = get_single_quote(self.kwargs.get('obj_id'))
        quote.id = quote._id
        
        return quote
    