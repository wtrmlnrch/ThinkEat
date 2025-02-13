from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
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