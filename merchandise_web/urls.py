from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('profil/', views.profile, name='profil'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.product_category, name='category'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_item/', views.updateItem, name='update_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('purchase/', views.purchase, name='purchase'),
]