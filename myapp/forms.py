import attrs
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from myapp.models import Caste, Photos, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control m-2"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control m-2"}))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', "placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', "placeholder": "Re enter Password"}),
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets={
            'username': forms.TextInput(attrs={"class": "form-control mb-2", "placeholder": "Username"}),
            'first_name': forms.TextInput(attrs={"class": "form-control mb-2", "placeholder": "First name"}),
            'last_name': forms.TextInput(attrs={"class": "form-control mb-2", "placeholder": "Last name"}),
            'email': forms.EmailInput(attrs={"class": "form-control mb-2", "placeholder": "Email"}),
        }
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
            'phone': forms.TextInput(attrs={"class": "form-control","placeholder": "Phone Number"}),
            'bio': forms.Textarea(attrs={"class": "form-control","placeholder": "Bio"}),
            'weight': forms.TextInput(attrs={"class": "form-control","placeholder": "Weight"}),
            'height': forms.TextInput(attrs={"class": "form-control","placeholder": "Height"}),
            'interest': forms.TextInput(attrs={"class": "form-control"})
        }


class UploadPhoto(forms.ModelForm):
    class Meta:
        model = Photos
        exclude = ['profile']