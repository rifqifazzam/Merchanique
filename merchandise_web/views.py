from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, Categorie, Profile, Order, OrderItem, Expedition, Shipment, Payment
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
from django.utils import timezone


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = request.POST['email']
            user.email = email
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            # render why error 
            errors = form.errors
            return render(request, 'register.html', {'form': form, 'errors': errors})
    elif request.method == 'GET':
        return render(request, 'register.html')

def index(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_total_items': 0}
        cartItems = order['get_total_items']
       
    products = Product.objects.all()
    categories = Categorie.objects.all()
    context = {
        'product': products,
        "categorie": categories,
        'cartItems': cartItems,
    }
    return render(request, 'homepage.html', context)

def loginview(request):
    form = UserCreationForm(request.POST)
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, f'Your account has been created! You are now able to log in')
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, f'Username OR password is incorrect')
            return render(request, 'login.html')
    
    elif request.method == 'GET':
        return render(request, 'login.html', )

def logoutview(request):
    logout(request)
    return redirect('homepage')

@login_required(login_url='login')
def profile(request):
    if request.method == 'GET':
        # Buat cart item di navbar
        if request.user.is_authenticated:
            user = request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_total_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_total_items': 0}
            cartItems = order['get_total_items']

        profile = Profile.objects.get(user=request.user)
        context = {
            'profile': profile,
            'cartItems': cartItems,
        }
        return render(request, 'profil.html', context)
    
    elif request.method == 'POST':
        # Buat cart item di navbar
        if request.user.is_authenticated:
            user = request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_total_items': 0}
            cartItems = order['get_total_items']

        # saving the full_name, nomor_tlp, and alamat
        profile = Profile.objects.get(user=request.user)
        profile.full_name = request.POST['full_name']
        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        # saving the image
        profile.image = request.FILES['image']        
        profile.save()

        context = {
            'profile': profile,
            'cartItems': cartItems,
        }
        return render(request, 'profil.html', context)

def product_detail(request, product_id):
    # Buat cart item di navbar
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_total_items': 0}
        cartItems = order['get_total_items']

    # Kode untuk menampilkan detail product
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
        'cartItems': cartItems,
    }
    return render(request, 'product_detail.html', context)

def product_category(request, category_id):
    # Buat cart item di navbar
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_total_items': 0}
        cartItems = order['get_total_items']

    # make this a page of item per category
    category = Categorie.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    
    context = {
        'product': products,
        'category': category,
        'cartItems': cartItems,
    }
    return render(request, 'product_category.html', context)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@login_required(login_url='login')
def add_to_cart(request, product_id):
    return render(request, 'my_cart.html')
    
# test
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def cart(request):
    user = request.user
    order, created = Order.objects.get_or_create(user=user, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_total_items    
    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'cart.html', context)

@login_required(login_url='login')
def checkout(request):
    if request.method == 'GET':
        expeditions = Expedition.objects.all()
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items 
        payments = Payment.objects.all()
        context = { 'expeditions': expeditions ,  'items' : items, 'order': order, 'payments' : payments}
        return render(request, 'checkout.html', context)
    elif request.method == 'POST':
       
        user = request.user
        city = request.POST['city']
        province = request.POST['province']
        zipcode = request.POST['zipcode']
        address = request.POST['address']
      
        order, created = Order.objects.get_or_create(user=user, complete=False)
        Shipment.objects.create(
            user=user,
            order=order,
            address=address,
            city=city,
            province=province,
            zipcode=zipcode,
        )

        payment_id = request.POST['payment']
        payment = Payment.objects.get(id=payment_id)
        # only update the order order_time
        order.order_time = timezone.now()
        order.payment = payment
        order.complete = True
        order.save()
        return redirect('purchase')

@login_required(login_url='login')
def purchase(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    # Query so it show the order item of the order
    order_items = []
    for order in orders:
        order_items.append(order.orderitem_set.all())

  
    context = { 'orders': orders, 'order_items': order_items}  
    return render(request, 'purchase.html', context)

# Jadi di checkout itu input shipment ama payment method ,trus create virutal ac  num
# @login_required(login_url='login')
# def processOrder(request):
#     data = json.loads(request.body)


    
#     return JsonResponse('Payment submitted..', safe=False)
