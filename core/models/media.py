from django.db import models
from .base import BaseModel
from .project import Project

class UploadedFile(BaseModel):
    STATUS_CHOICES = [("APPROVED", "approved"), ("REJECTED", "rejected"), ("SUBMITTED", "submitted")]

    file = models.FileField(upload_to="uploads/")
    original_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    status = models.CharField(choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.original_name} → {self.project}"