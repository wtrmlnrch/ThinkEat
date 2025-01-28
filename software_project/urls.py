from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("I cant figure out it this worked")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('', home, name='home'), 
]
