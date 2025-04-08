from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserUpdateForm(UserChangeForm):
    password = None  

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = { 
            'username': None,
        }
