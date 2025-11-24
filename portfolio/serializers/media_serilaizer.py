# api/serializers.py
from rest_framework import serializers
from core.models import UploadedFile
import os

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ["id", "file", "original_name", "file_type"]
        read_only_fields = ["original_name", "file_type"]

    def validate_file(self, value):
        if value.size > 3 * 1024 * 1024:
            raise serializers.ValidationError("File size must not exceed 3MB")

        filename = value.name
        if len(filename) > 50:
            raise serializers.ValidationError("Filename must not exceed 50 characters")

        if filename == filename.lower():
            raise serializers.ValidationError("Filename must contain at least one uppercase letter")

        ext = os.path.splitext(filename)[1].lower()
        allowed = [".png", ".jpg", ".jpeg", ".gif"]
        if ext not in allowed:
            raise serializers.ValidationError("Invalid file type")

        return value

    def create(self, validated_data):
        file = validated_data["file"]
        ext = file.name.split(".")[-1].lower()
        return UploadedFile.objects.create(
            file=file,
            original_name=file.name,
            file_type=ext,
        )
