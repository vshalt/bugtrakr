from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

User = get_user_model()


class Profile(models.Model):
    choices = (('submitter', 'Submitter'),
               ('developer', 'Developer'),
               ('manager', 'Manager'),
               ('admin', 'Admin'))

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    github = models.CharField(max_length=80, blank=True)
    roles = MultiSelectField(choices=choices, default='submitter')

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.id])
