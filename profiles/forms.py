# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile ,Poems

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email']






class PoemForm(forms.ModelForm):
    class Meta:
        model = Poems
        fields = ['title', 'poem']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove labels and set placeholders for each field
        self.fields['title'].label = ''
        self.fields['title'].widget.attrs['placeholder'] = 'Title'
        
        self.fields['poem'].label = ''
        self.fields['poem'].widget.attrs['placeholder'] = 'Write your Poem'

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.author = user
        if commit:
            instance.save()
        return instance


