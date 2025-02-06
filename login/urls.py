from django.urls import path
from . import views

urlpatterns = [
    path('landing_page/', views.landing_page, name='landing_page'),  # Root URL for landing page
    path('about/', views.about, name='about'),
    path('thinkeat/', views.thinkeat, name='thinkeat'),
    path('my-account/', views.my_account, name='my_account'),
]
