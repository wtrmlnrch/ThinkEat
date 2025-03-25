from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    

# Re-register UserAdmin with the new configuration
admin.site.register(CustomUser, CustomUserAdmin)
