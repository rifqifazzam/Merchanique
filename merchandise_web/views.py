from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, Categorie, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import ProfileUpdateForm
from django.contrib import messages

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
    products = Product.objects.all()
    categories = Categorie.objects.all()
    context = {
        'product': products,
        "categorie": categories,
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
        profile = Profile.objects.get(user=request.user)
        context = {
            'profile': profile,
        }
        return render(request, 'profil.html', context)
    elif request.method == 'POST':
        # p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        # if  p_form.is_valid():
        #     p_form.save()
        #     # messages.success(request, f'Your account has been updated!')
        #     return redirect('profil')


        # saving the full_name, nomor_tlp, and alamat
        profile = Profile.objects.get(user=request.user)
        profile.full_name = request.POST['full_name']
        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        # saving the image
        profile.image = request.FILES['image']        
        profile.save()

        context = {
            # 'p_form': p_form,
            'profile': profile,
        }
        return render(request, 'profil.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)

def product_category(request, category_id):
    # make this a page of item per category
    category = Categorie.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    
    context = {
        'product': products,
        'category': category,
    }
    return render(request, 'product_category.html', context)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()