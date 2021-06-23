from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from common.decorators import is_admin_or_manager
from .models import Comment
from tickets.models import Ticket
from .forms import CommentCreateForm


@login_required
@is_admin_or_manager
def comment_list(request):
    comments = Comment.objects.all()
    paginator = Paginator(comments, settings.COMMENTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, 'comments/list.html', {'comments': comments})


def comment_archive(request, id):
    tid = request.GET.get('tid')
    try:
        comment = Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        if comment.archived is True:
            comment.archived = False
        else:
            comment.archived = True
        comment.save()
        return redirect('tickets:detail', id=tid)


@login_required
def comment_create(request):
    tid = request.GET.get('tid')
    try:
        ticket = Ticket.objects.get(pk=tid)
    except Ticket.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = CommentCreateForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user.profile
            comment.save()
            return redirect('tickets:detail', id=tid)
    else:
        form = CommentCreateForm()
    return render(request, 'comments/create.html', {'form': form})


@login_required
def comment_edit(request, id):
    try:
        comment = Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        raise Http404
    tid = request.GET.get('tid')
    try:
        ticket = Ticket.objects.get(pk=tid)
    except Ticket.DoesNotExist:
        pass
    if request.method == 'POST':
        form = CommentCreateForm(data=request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(ticket.get_absolute_url())
    else:
        form = CommentCreateForm(instance=comment)
    return render(request, 'comments/edit.html', {'form': form})
