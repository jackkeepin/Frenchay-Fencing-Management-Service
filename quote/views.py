from django.shortcuts import render
from quote.models import Quote, get_all_quotes, get_single_quote, QuoteForm
from django.views.generic import DetailView, CreateView, DeleteView
from django.http import HttpResponse

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

    context = {
        'quotes': quotes
    }
    
    return render(request, 'quote/view_quotes.html', context)


class QuoteDetailView(DetailView):
    model = Quote

    def get_object(self, queryset=None):
        return get_single_quote(self.kwargs.get("obj_id"))


class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteForm

    def form_valid(self, form):
        return super().form_valid(form)

