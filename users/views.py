from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from core.views import home
from django.contrib.auth import authenticate, login, logout
from users.forms import  CustomRegistraionForm, RegisterForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def sign_up(request):
    form = CustomRegistraionForm()
    if request.method == 'POST':
        form = CustomRegistraionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(request, 'A confirmation mail sent. Please check your email')
            return redirect('sign-in')
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

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
    return redirect('sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'

    return render(request, 'admin/dashboard.html', {'users':users})


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to {role.name} role")
            return redirect('admin-dashboard')
    return render(request, 'admin/assign_role.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method =="POST":
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')
    
    return render(request, 'admin/create_group.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, group_id):
    group = Group.objects.get(id = group_id)
    if request.method == "POST":
        group_name = group.name
        group.delete()
        messages.success(request, f"{group_name} deleted successfully")
        return redirect('admin-dashboard')  


    return render(request, 'admin/delete_group.html', {'group': group})

@user_passes_test(is_admin, login_url='no-permission')
def delete_participants(request, user_id):
    participant = User.objects.get(id = user_id)
    if request.method == "POST":
        participant.delete()
        messages.success(request, f"{participant.username} deleted successfully")
        return redirect('admin-dashboard') 
    return render(request, 'admin/delete_participant.html', {'participant': participant})   




@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request,'admin/group_list.html', {'groups': groups})

@login_required
def rsvp_dashboard(request):
    rsvp_events = request.user.rsvp_events.all()
    return render(request, 'user/rsvp_dashboard.html', {'rsvp_events': rsvp_events})
    