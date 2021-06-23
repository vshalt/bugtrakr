from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect
from common.utils import get_user_roles, send_ticket_assign_email
from common.decorators import is_admin_or_manager
from projects.models import Project
from comments.models import Comment
from .models import Ticket, TicketHistory
from .forms import TicketCreateForm, TicketAssignForm


@login_required
def ticket_list(request):
    user, roles = get_user_roles(request)
    if 'admin' in roles:
        tickets = Ticket.objects.all()
    elif 'manager' in roles:
        projects = Project.objects.filter(users__id=user.profile.id)
        tickets = Ticket.objects.filter(project__in=projects)
    elif 'developer' in roles:
        tickets = Ticket.objects.filter(assigned_users__id=user.profile.id)
    else:
        tickets = Ticket.objects.filter(owner__id=user.profile.id)
    paginator = Paginator(tickets, settings.TICKETS_PER_PAGE)
    page = request.GET.get('page')
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)
    return render(request, 'tickets/list.html', {'tickets': tickets})


@login_required
def ticket_detail(request, id):
    user, roles = get_user_roles(request)
    try:
        ticket = Ticket.objects.get(pk=id)
    except Ticket.DoesNotExist:
        raise Http404
    comments = Comment.objects.filter(
        ticket=ticket, archived=False).order_by('-created')
    return render(request, 'tickets/detail.html',
                  {'ticket': ticket, 'comments': comments, 'roles': roles})


@login_required
def ticket_create(request):
    project_id = request.GET.get('pid')
    if request.method == 'POST':
        form = TicketCreateForm(
            project_id=project_id, request=request, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tickets:list')
    else:
        form = TicketCreateForm(
            project_id=project_id, request=request)
    return render(request, 'tickets/create.html', {'form': form})


@login_required
def ticket_edit(request, id):
    project_id = request.GET.get('pid')
    try:
        ticket = Ticket.objects.get(pk=id)
    except Ticket.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = TicketCreateForm(
            project_id=project_id, request=request, data=request.POST,
            instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('tickets:list')
    else:
        form = TicketCreateForm(
            project_id=project_id, request=request, instance=ticket)
    return render(request, 'tickets/edit.html', {'form': form})


@login_required
@is_admin_or_manager
def ticket_assign(request, id):
    try:
        ticket = Ticket.objects.get(pk=id)
    except Ticket.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = TicketAssignForm(request=request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket.assigned_user = cd['assigned_user']
            ticket.save()
            user = cd['assigned_user']
            send_ticket_assign_email(user, ticket)
            return redirect('tickets:list')
    else:
        form = TicketAssignForm(request=request)
    return render(request, 'tickets/assign.html', {'form': form})


def ticket_history(request, id):
    try:
        ticket = Ticket.objects.get(pk=id)
    except Ticket.DoesNotExist:
        raise Http404
    history = TicketHistory.objects.filter(ticket=ticket).order_by('-created')
    return render(request, 'tickets/history.html',
                  {'history': history, 'ticket': ticket})
