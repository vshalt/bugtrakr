from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Profile, User
from .forms import (
    RegisterForm, LoginForm, UserEditForm, ProfileEditForm, EditRolesForm)
from common.decorators import is_admin, is_admin_or_manager
from common.utils import get_user_roles
from projects.models import Project
from tickets.models import Ticket


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
    projects = Project.objects.filter(users__id=user.id)
    tickets = Ticket.objects.filter(
        Q(owner__id=user.profile.id) | Q(assigned_user__id=user.profile.id))
    return render(
        request, 'accounts/detail.html',
        {'user': user, 'tickets': tickets, 'projects': projects})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.set_password(cd['password1'])
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
            print(cd)
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


@login_required
def dashboard(request):
    user, roles = get_user_roles(request)
    if 'admin' in roles or user.is_superuser:
        projects = Project.objects.filter(archived=False)
        tickets = Ticket.objects.all()
    else:
        projects = Project.objects.filter(
            users__id=user.profile.id, archived=False)
        tickets = Ticket.objects.filter(
            Q(owner__id=user.profile.id) | Q(assigned_user__id=user.profile.id))
    return render(request, 'accounts/dashboard.html',
                  {'projects': projects, 'tickets': tickets})


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
                  {'form': [user_form, profile_form]})


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
            messages.success(request, 'Roles saved')
            return redirect('user_list')
    else:
        form = EditRolesForm(instance=user.profile)
    return render(request, 'accounts/roles.html',
                  {'form': form, 'roles': roles})


def demo(request):
    account = request.GET.get('acc')
    user = None
    if account == 'submitter':
        user = authenticate(request, username=settings.SUBMITTER_EMAIL,
                            password=settings.SUBMITTER_PASSWORD)
    if account == 'developer':
        user = authenticate(request, username=settings.DEVELOPER_EMAIL,
                            password=settings.DEVELOPER_PASSWORD)
    if account == 'manager':
        user = authenticate(request, username=settings.MANAGER_EMAIL,
                            password=settings.MANAGER_PASSWORD)
    if account == 'admin':
        user = authenticate(request, username=settings.ADMIN_EMAIL,
                            password=settings.ADMIN_PASSWORD)
    if user:
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/demo.html')


def home(request):
    return render(request, 'accounts/home.html')


@login_required
def apply_manager(request):
    request.user.profile.roles = 'submitter', 'developer', 'manager'
    request.user.profile.save()
    messages.success(request, 'You are now a project manager')
    return redirect('dashboard')


def error_404(request, exception=None):
    return render(request, 'errors/404.html')


def error_403(request, exception=None):
    return render(request, 'errors/403.html')


def error_500(request):
    return render(request, 'errors/500.html')
