from django.shortcuts import render
from quote.models import Quote, get_all_quotes, get_single_quote
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

# def view_quote(request, obj_id):
#     quote = get_single_quote(obj_id)
#     context = {
#         'quote': [vars(quote)]
#     }

#     return render(request, 'quote/view_quote.html', context)


class QuoteDetailView(DetailView):
    model = Quote
    # template_name = 'quote/quote_detail.html'

    def get_object(self, queryset=None):
        return get_single_quote(self.kwargs.get("obj_id"))


class QuoteCreateView(CreateView):
    model = Quote

    fields = [
        'customer_first_name',
        'customer_last_name',
        'customer_phone_num',
        'customer_email',
        'date_of_job',
        'job_description',
        'materials',
        'price_of_materials',
        'removal_included',
        'price_of_removal',
        'price_of_labour',
        'quote_price'
    ]

    def form_valid(self, form):
        # print(self.request)
        return super().form_valid(form)

