from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
        
    list_display = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'is_staff']

    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = list(UserAdmin.fieldsets) 
    personal_info = list(fieldsets[1][1]['fields'])
    personal_info.append('birth_date')
    fieldsets[1][1]['fields'] = tuple(personal_info)

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('birth_date',)}),
    )
    

# Re-register UserAdmin with the new configuration
admin.site.register(CustomUser, CustomUserAdmin)
