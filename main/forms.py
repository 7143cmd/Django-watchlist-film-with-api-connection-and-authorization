from .models import CustomUser
from django.forms import ModelForm, TextInput

class RegisterForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "username"
            }),
            "email": TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "email"
            }),
            "password": TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "password"
            })
        }

class LoginForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]

        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "username"
            }),
            "password": TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "password"
            })
        }