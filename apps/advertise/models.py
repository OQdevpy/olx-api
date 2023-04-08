from django.db import models
from datetime import date
from django.contrib.auth import get_user_model

from apps.accounts.models import Account
# from .categories import CATEGORY
# from apps.authentication.governrates import LOCATIONS
from .dates import Expire_date
# User = get_user_model()
# Create your models here.

class Category(models.Model):
    
        
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


class Advertise(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="advertise")
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name="advertise")
    # location = models.CharField(max_length= 200, choices = LOCATIONS)
    description = models.TextField(max_length=600)
    price = models.FloatField(max_length=100)
    expiration_date  = models.DateField(default = Expire_date, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_active']


    def __str__(self):
        return self.title

class Images(models.Model):
    advertise = models.ForeignKey(Advertise, related_name= 'images', on_delete = models.CASCADE)
    image  = models.ImageField(blank=True, null = True, upload_to='uploads/ads' ,default = '')