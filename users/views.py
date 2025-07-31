from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from core.views import home
from django.contrib.auth import authenticate, login, logout
from users.forms import  CustomRegistraionForm, RegisterForm, LoginForm
from django.contrib import messages


# Create your views here.

def sign_up(request):
    form = CustomRegistraionForm()
    if request.method == 'POST':
        form = CustomRegistraionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print('user', user)
            user.set_password(form.cleaned_data.get('password1'))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(request, 'A confirmation mail sent. Please check your email')
            return redirect('login')
        else:
            print('form is not valid')
    return render(request, 'registration/sign_up.html', {'form': form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
    return redirect('sign-in')