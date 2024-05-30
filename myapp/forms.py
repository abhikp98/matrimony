from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from myapp.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Password"}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']