from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import Project, User
from .utils import get_user_roles


def project_exists(f):
    @wraps(f)
    def wrap(request, id, *args, **kwargs):
        try:
            project = Project.objects.get(pk=id)
        except Project.DoesNotExist:
            raise Http404
        if request.user not in project.users.all():
            raise PermissionDenied
        return f(request, id, *args, **kwargs)
    return wrap


def is_admin_or_manager(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        user, roles = get_user_roles(request)
        if 'admin' in roles or 'manager' in roles or user.is_admin:
            return f(request, *args, **kwargs)
        return PermissionDenied
    return wrap


def is_manager(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        user, roles = get_user_roles(request)
        if 'manager' in roles:
            return f(request, *args, **kwargs)
        raise PermissionDenied
    return wrap


def is_admin(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        user, roles = get_user_roles()
        if 'admin' in roles or user.is_admin:
            return f(request, *args, **kwargs)
        raise PermissionDenied
    return wrap
