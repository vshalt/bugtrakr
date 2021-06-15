from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    # Registration and logins
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('edit/', views.user_login, name='edit'),

    # Change and reset password
    path('change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
