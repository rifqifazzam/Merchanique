from django.contrib import admin

# Register your models here.
from .models import Categorie, Product, Expedition, Profile, Order, OrderItem, Expedition, Payment, Shipment, ProductImg
admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(Expedition)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Shipment)
admin.site.register(ProductImg)

