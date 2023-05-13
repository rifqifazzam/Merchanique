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
    path('update_item2/', views.updateItem2, name='update_item2'),
    path('checkout/', views.checkout, name='checkout'),
    path('purchase/', views.purchase, name='purchase'),
    path('payment/<int:pk>/', views.payment, name='payment'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('order_detai/<int:pk>/', views.order_detail, name='order_detail'),
    path('process_order/<int:pk>/', views.process_order, name='process_order'),
    path('design/<int:pk>/', views.design, name='design'),
    path('design/<int:pk1>/delete-image/<int:pk2>/', views.delete_design_image, name='delete_design_image'),
    path('design/<int:pk1>/delete-text/<int:pk2>/', views.delete_design_text, name='delete_design_text'),
]