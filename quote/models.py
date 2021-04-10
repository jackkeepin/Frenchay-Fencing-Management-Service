from django.db import models
from djongo import models as djongomodels
from bson import ObjectId
from user.models import User


class Quote(models.Model):
    _id = djongomodels.ObjectIdField()
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    address = models.TextField() #this used to be JSONField, find something else
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone_num = models.CharField(max_length=15)
    materials = models.TextField() #this used to be JSONField, find something else
    job_description = models.TextField()
    date_of_job = models.DateField()
    price_of_materials = models.DecimalField(decimal_places=2)
    removal_included = models.BooleanField(default=False)
    price_of_removal = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    price_of_materials = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    price_of_labour = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    quote_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_first_name

def get_all_quotes():
    quotes = Quote.objects.all()
    return quotes.values()

def get_single_quote(object_id):
    quoteresp = Quote.objects.get(_id=ObjectId(object_id))
    return quoteresp