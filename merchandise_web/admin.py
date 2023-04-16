from django.contrib import admin

# Register your models here.
from .models import Categorie, Product, Expedition, Profile, Cart
admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(Expedition)
admin.site.register(Profile)
admin.site.register(Cart)

