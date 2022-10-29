from django.contrib.auth.models import User
from django.db import models

from project.models import Project


class Sheet(models.Model):
    sheet_date = models.DateField(null=False)
    sheet_start_time = models.TimeField(null=False)
    sheet_end_time = models.TimeField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sheets")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="sheets"
    )
