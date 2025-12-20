from django.conf import settings
from django.db import models
from .base import BaseModel
from .user import User

class Project(BaseModel):
    YEAR_CHOICES = [(1, "Year 1"), (2, "Year 2"), (3, "Year 3"), (4, "Year 4")]

    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    year = models.IntegerField(choices=YEAR_CHOICES)
    module = models.CharField(max_length=255)

    private = models.BooleanField(default=False)

    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="allowed_projects"
    )

    def __str__(self):
        return self.title
