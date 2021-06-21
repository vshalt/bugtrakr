from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render
from common.utils import get_user_roles
from projects.models import Project
from .models import Ticket
from .forms import TicketCreateForm


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
    try:
        ticket = Ticket.objects.get(pk=id)
    except Ticket.DoesNotExist:
        raise Http404
    return render(request, 'tickets/detail.html', {'ticket': ticket})


@login_required
def ticket_create(request):
    project_id = request.GET.get('pid')
    if request.method == 'POST':
        form = TicketCreateForm(
            project_id=project_id, request=request, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TicketCreateForm(
            project_id=project_id, request=request)
    return render(request, 'tickets/create.html', {'form': form})
