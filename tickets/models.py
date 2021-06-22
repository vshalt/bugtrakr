from django.db import models
from django.urls import reverse
from accounts.models import Profile
from projects.models import Project


class Ticket(models.Model):
    STATUS = (('new', 'New'), ('hold', 'On hold'), ('resolved', 'Resolved'),
              ('waiting', 'Waiting'))
    PRIORITY = (('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
                ('critical', 'Critical'))
    CLASSIFICATION = (('error', 'Error report'),
                      ('feature', 'Feature request'),
                      ('service', 'Service request'),
                      ('other', 'Other'))

    owner = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name='owned', default=None,
        null=True)
    assigned_user = models.ForeignKey(
        Profile, on_delete=models.PROTECT, default=None,null=True,
        related_name='assigned')
    title = models.CharField(max_length=80, null=False)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, related_name='tickets')
    priority = models.CharField(
        max_length=40, null=False, default="", choices=PRIORITY)
    status = models.CharField(max_length=40, choices=STATUS, default='New')
    classification = models.CharField(
        max_length=40, null=False, default="", choices=CLASSIFICATION)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tickets:detail', args=[self.id])


class TicketHistory(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.SET_NULL, default=None, null=True)
    user = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="")
