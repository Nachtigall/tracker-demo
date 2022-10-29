from django.contrib.auth.models import User
from rest_framework import serializers

from project.models import Project

from .models import Sheet


class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = "__all__"

    def create(self, validated_data):
        return Sheet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sheet_date = validated_data.get("sheet_date", instance.sheet_date)
        instance.sheet_start_time = validated_data.get(
            "sheet_start_time", instance.sheet_start_time
        )
        instance.sheet_end_time = validated_data.get(
            "sheet_end_time", instance.sheet_end_time
        )

        if instance.sheet_start_time > instance.sheet_end_time:
            raise serializers.ValidationError(
                "End time must be greater than start time"
            )

        instance.save()
        return instance

    def validate(self, data):
        """
        Check that the start is before the end.
        """
        if data.get("sheet_start_time", None) and data.get("sheet_end_time", None):
            if data["sheet_start_time"] > data["sheet_end_time"]:
                raise serializers.ValidationError(
                    "End time must be greater than start time"
                )
        return data
