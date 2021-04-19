from quote.models import Quote
from job.models import Job
from bson import ObjectId

def get_all_quotes():
    quotes = Quote.objects.all().order_by('date_of_job')
    return quotes

def get_single_quote(object_id):
    quoteresp = Quote.objects.get(_id=ObjectId(object_id))
    return quoteresp

def create_job_with_quote(quote):
    job = Job(
        customer_first_name = quote.customer_first_name,
        customer_last_name = quote.customer_last_name,
        address = quote.address,
        customer_email = quote.customer_email,
        customer_phone_num = quote.customer_phone_num,
        materials = quote.materials,
        job_description = quote.job_description,
        date_of_job = quote.date_of_job,
        removal_included = quote.removal_included,
        price_of_removal = quote.price_of_removal,
        price_of_materials = quote.price_of_materials,
        price_of_labour = quote.price_of_labour,
        job_price = quote.quote_price,
        issued_by = quote.issued_by
    )
    return job
