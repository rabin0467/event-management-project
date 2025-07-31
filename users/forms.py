from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission, Group
from events.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        print('this is help text zone')
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        

class CustomRegistraionForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'confirm_password', 'email']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1)< 8:
            raise forms.ValidationError('password must be at  least 8 character long')
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError('password must be include at least one uppercase letter')
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError('password must be include at least one lowercase letter')
        if not re.search(r'\d', password1):
            raise forms.ValidationError('password must be include at least one number letter')
        if not re.search(r'[!@#$%^&*()_+=<>?/|]', password1):
            raise forms.ValidationError('password must be include at least one special character')

        return password1
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email = email).exists()
        if email_exists:
            raise forms.ValidationError('Email already exists')
        return email
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 != confirm_password:
            raise forms.ValidationError('password did not match')
        
        return cleaned_data

class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
    
