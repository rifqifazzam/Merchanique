from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Categorie

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
        else:
            print(form.errors)
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request, 'register.html', {'form': form})
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
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    elif request.method == 'GET':
        return render(request, 'login.html', )

def logoutview(request):
    logout(request)
    return redirect('homepage')

@login_required(login_url='login')
def profil(request):
    return render(request, 'profil.html')


def product_detail(request):
    
    return render(request, 'product_detail.html')

def product_category(request):
    # make this a page of item per category
    categorie = Categorie.objects.get(id=1)
    context = {
        'categorie': categorie,
    }
    return render(request, 'product_category.html', context)