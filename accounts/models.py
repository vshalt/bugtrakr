from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Role(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.role}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    github = models.CharField(max_length=80, blank=True)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        return reverse("user_detail", args=[self.id])
