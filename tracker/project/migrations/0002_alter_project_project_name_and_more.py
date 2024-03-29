# Generated by Django 4.1.2 on 2022-10-29 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="project_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="project",
            name="project_owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
