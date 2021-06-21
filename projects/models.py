from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Profile

User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    users = models.ManyToManyField(Profile)

    class Meta():
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:detail', args=[self.id])
