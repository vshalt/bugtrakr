from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.contrib import messages

from accounts.models import Profile
from common.decorators import is_admin_or_manager
from common.utils import get_user_roles
from .forms import ProjectForm, AddUserForm, RemoveUserForm
from .models import Project, User


@login_required
def project_list(request):
    user, roles = get_user_roles(request)
    if 'admin' in roles:
        projects = Project.objects.filter(archived=False)
    else:
        projects = Project.objects.filter(
            users__id=request.user.profile.id, archived=False)
    paginator = Paginator(projects, settings.PROJECTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    print(request.get_host())
    return render(request, 'projects/list.html', {'projects': projects})


@login_required
def project_detail(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        raise Http404
    user, roles = get_user_roles(request)
    return render(request, 'projects/detail.html',
                  {'project': project, 'roles': roles})


@login_required
@is_admin_or_manager
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            project = form.save()
            project.users.add(request.user.profile)
            project.save()
            return redirect('projects:detail', id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/create.html', {'form': form})


@login_required
@is_admin_or_manager
def edit_project(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = ProjectForm(data=request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:detail', id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit.html', {'form': form})


@login_required
@is_admin_or_manager
def archived_projects(request):
    user, roles = get_user_roles(request)
    projects = Project.objects.filter(archived=True)
    paginator = Paginator(projects, settings.PROJECTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'projects/archived.html',
                  {'projects': projects, 'roles': roles})


@login_required
@is_admin_or_manager
def archive_project(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        if project.archived is False:
            project.archived = True
        else:
            project.archived = False
        project.save()
    return redirect('projects:list')

@login_required
@is_admin_or_manager
def assign_users(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        raise Http404
    project_users = project.users.all()
    all_users = User.objects.exclude(id__in=project_users)
    if request.method == 'POST':
        add_form = AddUserForm(project_users, data=request.POST)
        remove_form = RemoveUserForm(all_users, data=request.POST)
        if request.POST.get('assigned'):
            selected = request.POST.getlist('assigned')
            to_remove = Profile.objects.filter(id__in=selected)
            if remove_form.is_valid():
                for user in to_remove:
                    project.users.remove(user)
        if request.POST.get('all_users'):
            selected = request.POST.get('all_users')
            to_add = request.POST.getlist('all_users')
            if add_form.is_valid():
                for user in to_add:
                    project.users.add(user)
    else:
        add_form = AddUserForm(project_users)
        remove_form = RemoveUserForm(all_users)
    return render(
        request, 'projects/assign.html',
        {'add_form': add_form, 'remove_form': remove_form, 'project': project})
