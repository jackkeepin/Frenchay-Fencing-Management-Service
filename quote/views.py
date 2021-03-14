from django.shortcuts import render
from quote.models import Quote, get_all_quotes, get_single_quote
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

def view_quote(request, obj_id):
    quote = get_single_quote(obj_id)
    context = {
        'quote': [vars(quote)]
    }

    return render(request, 'quote/view_quote.html', context)
