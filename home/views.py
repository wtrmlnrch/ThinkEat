from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html')

def about(request):
    return render(request, 'about.html')

def thinkeat(request):
    return render(request, 'thinkeat.html')

def my_account(request):
    return render(request, 'my_account.html')

