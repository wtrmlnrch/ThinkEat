from django.contrib import admin
from django.urls import path
from ThinkEat.views import chat_view
from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
]


