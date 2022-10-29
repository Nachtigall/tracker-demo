from django.contrib.auth.models import User
from rest_framework import serializers

from project.models import Project
from sheet.models import Sheet


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "project_name", "project_owner_id"]


class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = [
            "id",
            "sheet_date",
            "sheet_start_time",
            "sheet_end_time",
            "project_id",
        ]


class UserSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    sheets = SheetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "projects", "sheets"]
