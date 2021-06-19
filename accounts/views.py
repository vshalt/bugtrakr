from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Profile, User
from .forms import (
    RegisterForm, LoginForm, UserEditForm, ProfileEditForm, EditRolesForm)
from projects.decorators import is_admin, is_admin_or_manager
from projects.utils import get_user_roles


def user_list(request):
    users = User.objects.all()
    paginator = Paginator(users, settings.USERS_PER_PAGE)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    roles = None
    if request.user.is_authenticated:
        user, roles = get_user_roles(request)
    return render(request, 'accounts/list.html',
                  {'users': users, 'roles': roles})


def user_detail(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        raise Http404
    return render(request, 'accounts/detail.html', {'user': user})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Account created, login to continue')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful')
                else:
                    messages.error(request, 'Account disabled')
            else:
                messages.error(request, 'Invalid account')
        return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('dashboard')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required
def user_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Account updated')
            return redirect('dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
@is_admin
def user_role(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        raise Http404
    roles = [role for role in user.profile.roles]
    if request.method == 'POST':
        form = EditRolesForm(data=request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = EditRolesForm(instance=user.profile)
    return render(request, 'accounts/roles.html',
                  {'form': form, 'roles': roles})

