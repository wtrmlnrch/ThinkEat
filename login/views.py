from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Test please work, literally if you don't I will cry")
 
def landing_page(request):
    return render(request, 'landing_page.html')