from django.db import models
from djongo import models as djongomodels
from bson import ObjectId
from user.models import User
from django.forms import ModelForm, CharField
from django.forms.widgets import DateInput
from django.urls import reverse

class Job(models.Model):
    _id = djongomodels.ObjectIdField()
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=1000, unique=True)
    customer_email = models.EmailField()
    customer_phone_num = models.CharField(max_length=15)
    materials = models.TextField()
    job_description = models.TextField()
    date_of_job = models.DateField()
    removal_included = models.BooleanField(default=False, null=True, blank=True)
    price_of_removal = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    price_of_materials = models.DecimalField(decimal_places=2, max_digits=6)
    price_of_labour = models.DecimalField(decimal_places=2, max_digits=6)
    job_price = models.DecimalField(decimal_places=2, max_digits=7)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_invoice = models.BooleanField(default=False)
    associated_quote = models.CharField(max_length=25)

    def __str__(self):
        return self.customer_first_name + " at " + self.address
    
    def get_absolute_url(self):
        return reverse('view-jobs')

class JobForm(ModelForm):

    street = CharField()
    city = CharField()
    post_code = CharField()

    def clean(self):
       street = self.cleaned_data['street']
       city = self.cleaned_data['city']
       post_code = self.cleaned_data['post_code']
       self.cleaned_data['address'] = street + ', ' + city + ', ' + post_code

       return self.cleaned_data

    class Meta:
        model = Job
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
            'job_price'
        ]
        widgets = {
            'date_of_job': DateInput(attrs={'type': 'date'}),
        }

