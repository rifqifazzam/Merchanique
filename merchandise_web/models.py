from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a category (e.g. T-Shirt, Hoodie, etc.)')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Categorie', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text='Enter description of the product', null=True, blank=True)
    image = models.ImageField(upload_to='images/category/', null=True, blank=True)
    
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
    
     # Override the save method of the model
    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # can have multiple products
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField()

    def __str__(self):
        # return cart_  + id
        return "Cart_" + str(self.id) 
        



