# api/serializers.py
import os
import mimetypes
from rest_framework import serializers
from core.models import UploadedFile, Project


class UploadedFileSerializer(serializers.ModelSerializer):
    # чтобы можно было прикреплять файл к проекту при создании
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = UploadedFile
        fields = ["id", "project", "file", "original_name", "file_type"]
        read_only_fields = ["original_name", "file_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Lazy import, чтобы не ловить циклические импорты
        from core.models import Project
        self.fields["project"].queryset = Project.objects.all()

    def validate_file(self, value):
        # 25 MB — адекватно для портфолио, поменяй если хочешь
        max_size = 25 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("File size must not exceed 25MB")

        filename = value.name or ""
        if len(filename) > 255:
            raise serializers.ValidationError("Filename is too long (max 255 chars)")

        # Разрешённые расширения под требования (PDF, Office, картинки, txt/zip по желанию)
        allowed_exts = {
            ".pdf",
            ".doc", ".docx",
            ".ppt", ".pptx",
            ".xls", ".xlsx",
            ".odt", ".ods", ".odp",
            ".png", ".jpg", ".jpeg", ".gif", ".webp",
            ".txt",
            ".zip",
        }

        ext = os.path.splitext(filename)[1].lower()
        if not ext:
            raise serializers.ValidationError("File must have an extension (e.g. .pdf)")

        if ext not in allowed_exts:
            raise serializers.ValidationError(
                f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(allowed_exts))}"
            )

        # Мягкая проверка mime (не 100% защита, но норм как дополнительная)
        guessed_mime, _ = mimetypes.guess_type(filename)
        if guessed_mime is None:
            # не валим загрузку, просто пропускаем
            return value

        blocked_mimes = {
            "application/x-msdownload",  # exe
            "application/x-sh",          # shell scripts
        }
        if guessed_mime in blocked_mimes:
            raise serializers.ValidationError("This file type is not allowed")

        return value

    def create(self, validated_data):
        f = validated_data["file"]
        filename = os.path.basename(f.name)
        ext = os.path.splitext(filename)[1].lower().lstrip(".")
        return UploadedFile.objects.create(
            project=validated_data["project"],
            file=f,
            original_name=filename,
            file_type=ext,
        )
