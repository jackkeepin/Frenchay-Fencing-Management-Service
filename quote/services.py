from quote.models import Quote
from bson import ObjectId

def get_all_quotes():
    quotes = Quote.objects.all()
    # return quotes.values()
    return quotes

def get_single_quote(object_id):
    quoteresp = Quote.objects.get(_id=ObjectId(object_id))
    return quoteresp