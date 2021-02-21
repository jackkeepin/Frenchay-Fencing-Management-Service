from django.shortcuts import render
# from django.http import HttpResponse

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
    return render(request, 'quote/view_quotes.html')