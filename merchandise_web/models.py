from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a category (e.g. T-Shirt, Hoodie, etc.)')
    image = models.ImageField(upload_to='images/category/', null=True, blank=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    category = models.ForeignKey('Categorie', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text='Enter description of the product', null=True, blank=True)
    image = models.ImageField(upload_to='images/product/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

class Expedition(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/profil_image/', default='default.jpg')

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # can have multiple products
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField()

    def __str__(self):
        # return cart_  + id
        return "Cart_" + str(self.id) 
        



