from django.contrib import admin
from .models import Ticket, TicketHistory


admin.site.register(Ticket)
admin.site.register(TicketHistory)
