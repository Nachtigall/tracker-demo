from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    project_name = models.CharField(max_length=50)
    project_description = models.CharField(max_length=200, blank=True)
    project_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="projects", blank=True)
