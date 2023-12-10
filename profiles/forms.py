# forms.py
from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
