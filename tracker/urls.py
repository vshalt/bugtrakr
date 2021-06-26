"""tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler403, handler500
from accounts import views as account_views

urlpatterns = [
    path('', account_views.home, name='home'),
    path('dashboard/', account_views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('tickets/', include('tickets.urls', namespace='tickets')),
    path('comments/', include('comments.urls', namespace='comments')),
]

handler403 = account_views.error_403
handler404 = account_views.error_404
handler500 = account_views.error_500

