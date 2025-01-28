from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# A simple view for the root path
def home(request):
    return HttpResponse("Welcome to the Home Page!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/logout URLs
    path('', home, name='home'),  # Add this for the root path
]
