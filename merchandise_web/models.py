from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

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
    designable = models.BooleanField(default=False, null=True, blank=False)
    variantble = models.BooleanField(default=True, null=True, blank=False)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self): 
        return self.name
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])
    
class ProductImg(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/product/', null=True, blank=True)
    
    def __str__(self):
        return self.product.name + ' - ' + str(self.id)
    
class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('9oz', 'Small size with a capacity of 9 ounces'),
        ('16oz', 'Medium size with a capacity of 16 ounces'),
        ('25oz', 'Medium size with a capacity of 25 ounces'),
        ('32oz', 'Medium size with a capacity of 32 ounces'),
        ('60oz', 'Large size with a capacity of 60 ounces'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', null=True, blank=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=5)
    # stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.get_size_display()}"

class Expedition(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/expedition/', null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)

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
    
class Payment(models.Model):
    name = models.CharField(max_length=200, null=True) 
    number = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='images/payment/', null=True, blank=True)
    bank_code = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return self.name
    
class UserDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/user_design/', null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    design_option = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return str(self.id)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True ,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    order_id = models.CharField(max_length=200, null=True)
    expedition = models.ForeignKey(Expedition, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    payment_status = models.BooleanField(default=False, null=True, blank=False)
    virtual_account = models.CharField(max_length=200, null=True, blank=True)

    full_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)    
    
    def __str__(self):
        return str(self.id)
    
    def getno():
        return models.Model;
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
       
    @property
    def get_total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 
    
    @property
    def get_total_payment(self):
        total = self.get_cart_total + self.expedition.price
        return total
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user_design = models.ForeignKey(UserDesign, on_delete=models.SET_NULL, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True) # New field for variant
    order_id2 = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self): 
        return str(self.id)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        if self.user_design:
            total += self.user_design.price
        return total
    
    
    
 
class Shipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    province = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    tracking_number = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.address

