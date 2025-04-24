from django.urls import path
from . import views
from .views import tutorial_view

urlpatterns = [
    path('thinkeat/', views.thinkeat, name='thinkeat'),
    path('tutorial/', tutorial_view, name='tutorial'),
    path('my-account/', views.my_account, name='my_account'),
    path('register/', views.register, name="register"),
    path('braxton-secret/', views.secret_page, name='secret_page')
]
