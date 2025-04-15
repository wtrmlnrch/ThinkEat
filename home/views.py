from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CustomUserUpdateForm

def landing_page(request):
    return render(request, 'home_page/landing_page.html')

def about(request):
    return render(request, 'home_page/about.html')

def thinkeat(request):
    return render(request, 'thinkeat.html')

def tutorial_view(request):
    return render(request, 'home_page/tutorial.html')

def secret_page(request):
    return render(request, 'home_page/secret.html')


def my_account(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid() and form.has_changed():
            form.save()
            messages.success(request, "Your information has been successfully updated.")
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'registration/my_account.html', {'form':form})

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
        birth_date = request.POST.get('birth_date')
       
        if not all([first_name, last_name, username, password, email]):
            messages.error(request, "All fields are required!")
            return render(request, 'registration/registration.html', status=400)
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'registration/registration.html', status=400)

        try:
            birth_date_parsed = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid birth date format.")
            return render(request, 'registration/registration.html', status=400)

        CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date_parsed
        )
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('/login/')

    return render(request, 'registration/registration.html')
