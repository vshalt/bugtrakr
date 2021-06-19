from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField

User = get_user_model()


class Profile(models.Model):
    choices = (('submitter', 'Submitter'),
               ('developer', 'Developer'),
               ('manager', 'Manager'),
               ('admin', 'Admin'))

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    github = models.CharField(max_length=40, blank=True)
    roles = MultiSelectField(choices=choices, default='submitter')
