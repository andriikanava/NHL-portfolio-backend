from django.db import models
from .base import BaseModel

class Project(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
