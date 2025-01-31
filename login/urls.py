from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.landing_page, name="landing_page"),
    path("landing_page/",views.landing_page, name="landing_page"),
    path("login/about/",views.about, name="about"),

   
    
]