from django.db import models
from .base import BaseModel
from .project import Project

class UploadedFile(BaseModel):
    file = models.ImageField(upload_to="uploads/")
    original_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return f"{self.original_name} → {self.project}"