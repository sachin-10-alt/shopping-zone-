
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserForm(UserCreationForm):
  username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter User Name'}))

  class Meta:
    model=User
    fields=['username', 'email', 'password1', 'password2']