from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *

def landing_page(request):
    return render(request, 'home_page/landing_page.html')

def about(request):
    return render(request, 'home_page/about.html')

def thinkeat(request):
    return render(request, 'thinkeat.html')

def my_account(request):
    return render(request, 'registration/my_account.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login/')
        user = authenticate(username=username,password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/landing_page/')
        
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email_address = request.POST.get('email_address')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username)

        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully!")
        return render(request, 'registration/registration.html')
    
    return render(request, 'registration/registration.html')
