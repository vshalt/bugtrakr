from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

router = routers.DefaultRouter()
router.register("", views.UserDetailViewSet, basename="all_users")
router.register("", views.AuthenticatedUserViewSet, basename="authenticated_users")


urlpatterns = [
    # Registration and logins
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("demo/", views.demo, name="demo"),
    # TODO: change
    path("apply/", views.apply_manager, name="apply"),
    # Change and reset password
    path("change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path(
        "change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("", include(router.urls)),
]
