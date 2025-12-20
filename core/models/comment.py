from django.db import models
from .base import BaseModel
from .project import Project
from .user import User

class Comment(BaseModel):
    STATUS_CHOICES = [("OPEN", "open"), ("CLOSE", "close")]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.TextField(null=False, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    status = models.CharField(choices=STATUS_CHOICES)


    def __str__(self):
        return f"{self.comment} → {self.project}"
