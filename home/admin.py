from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Define an inline admin descriptor for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"

# Extend the UserAdmin class to include UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)  # Add the profile inline to Users

# Re-register UserAdmin with the new configuration
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
