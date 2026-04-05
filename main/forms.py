from .models import CustomUser
from django.forms import ModelForm, TextInput, Form, PasswordInput, CharField

class RegisterForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

        labels = {
            "username": "",
            "email": "",
            "password": "",
        }

        widgets = {

            "username": TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "username"
            }),
            "email": TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "email"
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "password"
            })
        }

class LoginForm(Form):
    username = CharField(
        label = '',
        max_length=20,
        widget=TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'username'
        })
    )

    password = CharField(
        label = '',
        widget=PasswordInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'password'
        })
    )