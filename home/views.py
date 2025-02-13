from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def landing_page(request):
    return render(request, 'home_page\landing_page.html')

def about(request):
    return render(request, 'home_page/about.html')

def thinkeat(request):
    return render(request, 'thinkeat.html')

def my_account(request):
    return render(request, 'registration\my_account.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['text']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(landing_page)
        else:
            return render(request, 'login.html', {'error': 'Nuhuh'})
    return render(request, 'login.html')
