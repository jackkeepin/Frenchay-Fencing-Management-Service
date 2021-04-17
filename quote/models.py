from django.db import models
from djongo import models as djongomodels
from bson import ObjectId
from user.models import User
from django.urls import reverse
from django.forms import ModelForm
from django.forms.widgets import DateInput

class Quote(models.Model):
    _id = djongomodels.ObjectIdField()
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=1000)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone_num = models.CharField(max_length=15)
    materials = models.TextField(null=True, blank=True)
    job_description = models.TextField()
    date_of_job = models.DateField(null=True, blank=True)
    price_of_materials = models.DecimalField(decimal_places=2)
    removal_included = models.BooleanField(default=False, null=True, blank=True)
    price_of_removal = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    price_of_materials = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    price_of_labour = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    quote_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_first_name + " at " + self.address
    
    def get_absolute_url(self):
        ##cannot redirect to just created obj because mongo ObjectId is assigned by db
        return reverse('view-quotes')


class QuoteForm(ModelForm):

    class Meta:
        model = Quote
        fields = [
            'customer_first_name',
            'customer_last_name',
            'customer_phone_num',
            'customer_email',
            'address',
            'date_of_job',
            'job_description',
            'materials',
            'price_of_materials',
            'removal_included',
            'price_of_removal',
            'price_of_labour',
            'quote_price'
        ]
        widgets = {
            'date_of_job': DateInput(attrs={'type': 'date'}),
        }


def get_all_quotes():
    quotes = Quote.objects.all()
    # return quotes.values()
    return quotes

def get_single_quote(object_id):
    quoteresp = Quote.objects.get(_id=ObjectId(object_id))
    return quoteresp