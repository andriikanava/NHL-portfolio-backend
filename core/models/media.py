from django.db import models
from .base import BaseModel

class UploadedFile(BaseModel):
    file = models.ImageField(upload_to="uploads/")
    original_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)

    def __str__(self):
        return self.original_name