# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class UserForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address...'})
    )
    # phone = forms.CharField(
    #     max_length=25, required=False,
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number...'})
    # )
    # username = forms.CharField(
    #     max_length=255, required=False,
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username...'})
    # )
    handle = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Handle...'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password...'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password...'})
    )
    # first_name = forms.CharField(
    #     max_length=255, required=False,
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name...'})
    # )
    # last_name = forms.CharField(
    #     max_length=255, required=False,
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name...'})
    # )



class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Email Address...'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'})
    )


