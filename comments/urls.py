from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('', views.comment_list, name='list'),
    path('create/', views.comment_create, name='create'),
    path('edit/<int:id>/', views.comment_edit, name='edit'),
    path('archive/<int:id>/', views.comment_archive, name='archive'),
]
