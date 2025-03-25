from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
#comment
def landing_page(request):
    return render(request, 'home_page/landing_page.html')

def about(request):
    return render(request, 'home_page/about.html')

def thinkeat(request):
    return render(request, 'thinkeat.html')

def my_account(request):
    return render(request, 'registration/my_account.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not CustomUser.objects.filter(username=username).exists():
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
        email = request.POST.get('email_address')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('/register/')

        # Create the user and its profile
        CustomUser.objects.create_user(username=username, password=password, email=email, 
                                       first_name=first_name, last_name=last_name)

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('/login/')

    return render(request, 'registration/registration.html')