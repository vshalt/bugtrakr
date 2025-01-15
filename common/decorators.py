from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.permissions import BasePermission

from common.utils import get_user_roles
from projects.models import Project, User


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
        if "admin" in roles or "manager" in roles or user.is_superuser:
            return f(request, *args, **kwargs)
        raise PermissionDenied

    return wrap


def is_manager(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        user, roles = get_user_roles(request)
        if "manager" in roles:
            return f(request, *args, **kwargs)
        raise PermissionDenied

    return wrap


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        user, roles = get_user_roles(request)
        return "admin" in roles or user.is_superuser


def is_admin(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        user, roles = get_user_roles(request)
        if "admin" in roles or user.is_superuser:
            return f(request, *args, **kwargs)
        raise PermissionDenied

    return wrap
