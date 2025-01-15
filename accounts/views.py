from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from common.decorators import IsAdminUserRole
from serializers import (EditUserSerializer, LoginSerializer,
                         RegisterUserSerializer, UpdateRoleSerializer,
                         UserDetailSerializer, UserSerializer)

from .models import Role, User


class UserDetailViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"])
    def users(self, request):
        paginator = PageNumberPagination()
        limit = request.query_params.get("limit", settings.USERS_PER_PAGE)
        paginator.page_size = limit
        users = User.objects.all()
        users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(users, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"])
    def details(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        return Response(UserDetailSerializer(user).data)

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.profile.roles.add(Role.objects.get(id=1))
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {"refresh": str(refresh), "access": str(refresh.access_token)}
                    )
                else:
                    return Response(
                        {"error": "Account disabled"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedUserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        user = request.user
        return Response(UserDetailSerializer(user).data)

    @action(detail=False, methods=["post"])
    def edit(self, request):
        user = request.user
        serializer = EditUserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated, IsAdminUserRole],
    )
    def update_role(self, request):
        serializer = UpdateRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: demo accounts
def demo(request):
    account = request.GET.get("acc")
    user = None
    if account == "submitter":
        user = authenticate(
            request,
            username=settings.SUBMITTER_EMAIL,
            password=settings.SUBMITTER_PASSWORD,
        )
    if account == "developer":
        user = authenticate(
            request,
            username=settings.DEVELOPER_EMAIL,
            password=settings.DEVELOPER_PASSWORD,
        )
    if account == "manager":
        user = authenticate(
            request, username=settings.MANAGER_EMAIL, password=settings.MANAGER_PASSWORD
        )
    if account == "admin":
        user = authenticate(
            request, username=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD
        )
    if user:
        login(request, user)
        return redirect("dashboard")
    return render(request, "accounts/demo.html")


def home(request):
    return render(request, "accounts/home.html")


@login_required
def apply_manager(request):
    request.user.profile.roles = "submitter", "developer", "manager"
    request.user.profile.save()
    messages.success(request, "You are now a project manager")
    return redirect("dashboard")


def error_404(request, exception=None):
    return render(request, "errors/404.html")


def error_403(request, exception=None):
    return render(request, "errors/403.html")


def error_500(request):
    return render(request, "errors/500.html")
