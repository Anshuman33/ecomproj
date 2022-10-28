from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(null=False,blank=False, max_length=50)
    phone_number = models.CharField(max_length=10)
    first_name = models.CharField(blank=False, max_length=20)
    last_name = models.CharField(blank=True, max_length=20)
    address = models.TextField()
    city = models.CharField()
    state = models.CharField()
    pincode = models.CharField()
    

class Supplier(models.Model):
    pass
    
    
