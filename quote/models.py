from django.db import models


class Quote(models.Model):
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    address = models.JSONField(null=True, blank=True)
    customer_email = models.EmailField()
    materials = models.JSONField(null=True, blank=True)
    job_descripton = models.TextField()
    dateOfJob = models.DateField()
    price_of_materials = models.DecimalField(decimal_places=2)
    removal_included = models.BooleanField(null=True, blank=True)
    price_of_materials = models.DecimalField(decimal_places=2, max_digits=6)
    price_of_labour = models.DecimalField(decimal_places=2, max_digits=6)
    quote_price = models.DecimalField(decimal_places=2, max_digits=6)
    issued_by = models.CharField(max_length=255)
    issued_by_phone_num = models.CharField(max_length=15)

