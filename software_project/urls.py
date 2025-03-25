from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from home import views

urlpatterns = [
    path('landing_page/', views.landing_page, name='landing_page'),  # Root URL for landing page
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Include auth URLs
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', RedirectView.as_view(url='/login/')),  # Redirect root to login
    path('', include('home.urls')),
    path('',include('ThinkEat.urls'))
]
