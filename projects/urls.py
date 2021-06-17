from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('detail/<int:id>', views.project_detail, name='detail'),
    path('create/', views.project_create, name='create'),
    path('edit/<int:id>', views.edit_project, name='edit'),
    path('archived/', views.archived_projects, name='archived'),
    path('assign/<int:id>', views.assign_users, name='assign'),
]
