from django.db import models

# Create your models here.
class Quote(models.Model):
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    address = {}
    customer_email = models.EmailField()
    materials = {}
    job_descripton = models.TextField()
    price_of_materials = models.DecimalField(decimal_places=2)
    removal_included = models.BooleanField(null=True, blank=True)
    price_of_materials = models.DecimalField(decimal_places=2)
    price_of_labour = models.DecimalField(decimal_places=2)
    quote_price = models.DecimalField(decimal_places=2)
    issued_by = models.CharField(max_length=255)
    issued_by_phone_num = models.CharField(max_length=15)

class Address(models.Model):
    address_line_one = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    postcode = models.CharField(max_length=10)