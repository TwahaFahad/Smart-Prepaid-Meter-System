from django.db import models
from django.conf import settings

from payments.helpers import generate_reference

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, blank=True)
    address1 = models.CharField(max_length=250,blank=True)
    address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    country_code =models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=2)
    order_key = models.CharField(max_length=200, default=generate_reference())
    payment_option = models.CharField(max_length=255, blank=True)
    billing_status = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    

class ElectrictyCost(models.Model):
    price_per_kwh = models.DecimalField(decimal_places=2, max_digits=7)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.price_per_kwh)

