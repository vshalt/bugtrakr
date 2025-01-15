from django.db import models

from accounts.models import Profile
from tickets.models import Ticket


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket, related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Profile, related_name="comments", on_delete=models.SET_NULL, null=True
    )
    body = models.TextField()
    archived = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.ticket}"

    class Meta:
        ordering = ("-created",)
