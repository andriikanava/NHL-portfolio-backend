from django.db import models
from .base import BaseModel

class Comment(BaseModel):
    ROLE_CHOICE = [
        ("student", "Student"),
        ("teacher", "Teacher")
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    comment = models.TextField(null=False, blank=False)
    role = models.CharField(choices=ROLE_CHOICE, null=False, blank=False)
    notify = models.BooleanField(null=False, blank=False, default=False)


    def __str__(self):
        return self.title
