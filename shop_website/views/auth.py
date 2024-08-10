from django.shortcuts import render
from shop_website.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect

def login_page(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('product_list')
            else:
                messages.error(request, 'Invalid username or password')

    return render(request,'shop_website/auth/login.html', {'form': 'form'})


def logout_page(request):
    logout(request)
    return redirect('product_list')

def register_page(request):
    return render(request, 'shop_website/auth/login.html')