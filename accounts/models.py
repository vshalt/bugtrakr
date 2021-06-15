from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField


class Profile(models.Model):
    choices = (('submitter', 'Submitter'),
               ('developer', 'Developer'),
               ('manager', 'Manager'),
               ('admin', 'Admin'))

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    github = models.CharField(max_length=40, blank=True)
    roles = MultiSelectField(choices=choices, default='submitter')
