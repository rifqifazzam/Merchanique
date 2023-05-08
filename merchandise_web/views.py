from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, Categorie, Profile, Order, OrderItem, Expedition, Shipment, Payment, ProductImg, UserDesign
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
import json
import random
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404



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
        if request.user.is_authenticated:
            # Showing the total cart items in navbar
            user = request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_total_items
        else:
            # Case where user is not logged in
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
        # Showing the total cart items in navbar
        if request.user.is_authenticated:
            user = request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_total_items
        else:
            # Case where user is not logged in
            items = []
            order = {'get_cart_total': 0, 'get_total_items': 0}
            cartItems = order['get_total_items']

        # Updating the user profile
        profile = Profile.objects.get(user=request.user)
        profile.full_name = request.POST['full_name']
        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
 
        # Handle the case where no image is uploaded
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
        else:
            # Use the old image if available
            if profile.image:
                profile.image = profile.image

        profile.save()

        # Update the username and email
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()

        context = {
            'profile': profile,
            'cartItems': cartItems,
        }
        return render(request, 'profil.html', context)

def product_detail(request, product_id):
    # Showing the total cart items in navbar
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
    product_images = ProductImg.objects.filter(product=product)
    context = {
        'product': product,
        'cartItems': cartItems,
        'product_images': product_images,
    }
    return render(request, 'product_detail.html', context)

def product_category(request, category_id):
    # Showing the total cart items in navbar
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_total_items': 0}
        cartItems = order['get_total_items']

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
        messages.success(request, f'Item was successfully added')
        orderItem.save()
        # Render message item suces fully added
        return JsonResponse({'success': 'Item was added'}, status=200)

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
        context = { 'expeditions': expeditions ,  'items' : items, 'order': order, 'payments' : payments,  'cartItems': cartItems,}
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
        expedition_id = request.POST.get('expedition')
        expedition = Expedition.objects.get(id=expedition_id)
        order.expedition = expedition

        # Generate the virtual account number
        random_num = str(random.randint(100, 999))
        bank_code = payment.bank_code  # Get the bank code from the payment object
        virtual_account = bank_code + str(order.order_id) + random_num

        # Save the virtual account number in the order object
        order.virtual_account = virtual_account

        order.date_ordered = timezone.now()
        order.payment = payment
        order.complete = True
        order.save()
        return redirect('purchase')

@login_required(login_url='login')
def purchase(request):
    user = request.user
    
    orders = Order.objects.filter(user=user, orderitem__quantity__gt=0).distinct()
    order_items = []
    for order in orders:
        order_items.append(order.orderitem_set.all())

    shipments = Shipment.objects.filter(user=user, order__payment_status=True)   
    context = { 'orders': orders, 'order_items': order_items, 'shipments': shipments,}  
    return render(request, 'purchase.html', context)


@login_required(login_url='login')
def payment(request, pk):
    # get hthe order by the user request
    user = request.user
    order = Order.objects.get(id=pk)
    context = {'order': order}

    
    return render(request, 'payment.html', context)
 

#  Admin views
@user_passes_test(lambda u: u.is_superuser)
def manage_orders(request):
    orders = Order.objects.all()
    total_sent = Order.objects.filter(payment_status=True).count()
    # the unpaid orders
    total_unpaid = Order.objects.filter(payment_status=False).count()
    context = {'orders': orders, 'total_sent': total_sent, 'total_unpaid': total_unpaid}
    return render(request, 'manage_orders.html', context)

@user_passes_test(lambda u: u.is_superuser)
def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    shipment = Shipment.objects.get(order=order)
    # get the expedition object
    expedition = Expedition.objects.get(id=order.expedition.id)
    context = {'order': order, 'shipment': shipment, 'expedition': expedition}
    return render(request, 'order_detail.html', context)

# Make a process order
@user_passes_test(lambda u: u.is_superuser)
def process_order(request, pk):
    order = Order.objects.get(id=pk)
    shipment = Shipment.objects.get(order=order)
    if request.method == 'POST':
        order.payment_status = True
        tracking_number = request.POST['tracking_number']
        shipment.tracking_number = tracking_number
        
        
        order.save()
        shipment.save()
        return redirect('manage_orders')
    
@login_required(login_url='login')
def design(request, pk):
    orderitem = OrderItem.objects.get(id=pk)
    if request.method == 'POST':
        design_image = request.FILES.get('design_image')
        design_text = request.POST.get('design_text')

        # check if order item already has a user design
        if orderitem.user_design:
            # update existing user design
            user_design = orderitem.user_design
            user_design.image = design_image or user_design.image # use new image or existing image
            user_design.text = design_text
            user_design.save()
        else:
            # create a new user design and associate it with the order item
            user_design = UserDesign.objects.create(
                user=request.user,
                image=design_image,
                text=design_text,
                price=orderitem.product.price
            )
            orderitem.user_design = user_design
            orderitem.save()

        # redirect to the cart page
        return redirect(request.path)
    
    else:
        # if not a POST request, display the design page with the order item
        context = {'orderitem': orderitem} 
        return render(request, 'design.html', context)


def delete_design_image(request, pk):
    user_design = get_object_or_404(UserDesign, pk=pk, user=request.user)
    orderitem_id = user_design.orderitem.id 
    if request.method == 'POST':
        # delete the image file and the UserDesign instance
        user_design.image.delete()
        return redirect('design', pk=orderitem_id) 
    


@login_required(login_url='login')
def delete_design_text(request, pk):
    user_design = get_object_or_404(UserDesign, pk=pk, user=request.user)
    orderitem_id = user_design.orderitem.id 
    if request.method == 'POST':
        # delete the UserDesign instance
        user_design.text = None
        user_design.save()
        return redirect('design', pk=orderitem_id) 
