from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from login import views

urlpatterns = [
    path('landing_page/', views.landing_page, name='landing_page'),  # Root URL for landing page
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include auth URLs
    path('', RedirectView.as_view(url='/accounts/login/')),  # Redirect root to login
    path('', include('login.urls')),
]
