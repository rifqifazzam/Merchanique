from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('profil/', views.profil, name='profil'),
    path('product_detail/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.product_category, name='category'),

]