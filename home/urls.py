from django.urls import path
from . import views

urlpatterns = [
    path('thinkeat/', views.thinkeat, name='thinkeat'),
    path('my-account/', views.my_account, name='my_account'),
]
