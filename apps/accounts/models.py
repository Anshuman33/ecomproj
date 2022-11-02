from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True)
    name = models.CharField(max_length = 100, null=False, blank=False)
    phone = models.CharField(unique = True, max_length=10)
    is_buyer = models.BooleanField(default = True)
    is_seller = models.BooleanField(default = False)
    address = models.TextField(null = True, blank = True)
    city = models.CharField(max_length = 40,null = True, blank = True)
    state = models.CharField(max_length = 40, null = True, blank = True)
    pincode = models.CharField(max_length = 6, null = True, blank = True)
    last_login_time = models.DateTimeField(null = True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_subscribed = models.BooleanField(default = False)
    
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    
    