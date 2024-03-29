# Generated by Django 4.1.2 on 2022-10-29 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0002_alter_project_project_name_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sheet", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sheet",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sheets",
                to="project.project",
            ),
        ),
        migrations.AlterField(
            model_name="sheet",
            name="sheet_end_time",
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name="sheet",
            name="sheet_start_time",
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name="sheet",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sheets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
