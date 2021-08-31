from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'autofocus': 'autofocus',
        }),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'autofocus': 'autofocus',
        }),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'placeholder': 'First Name',
                'autofocus': 'autofocus',
            }),
            'last_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'placeholder': 'Last Name',
                'autofocus': 'autofocus',
            }),
            'email': forms.EmailInput(attrs={
                'type': 'email',
                'class': "form-control",
                'placeholder': 'Email',
                'autofocus': 'autofocus',
            }),
        }
