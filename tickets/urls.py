from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    # path('', views.ticket_list, name='list'),
    path('create/', views.ticket_create, name='create'),
    # path('edit/<int:id>', views.ticket_edit, name='edit'),
    # path('detail/<int:id>', views.ticket_detail, name='detail'),
    # path('assign/<int:id>', views.ticket_assign, name='assign'),
    # path('confirm/', views.ticket_confirm, name='confirm'),
    # path('history/', views.ticket_history, name='history'),
]
