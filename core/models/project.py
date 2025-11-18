from django.db import models
from .base import BaseModel

class Project(BaseModel):
    PERIOD_CHOICES = [
        (1, "1 period"),
        (2, "2 period"),
        (3, "3 period"),
        (4, "4 period"),
    ]

    WEEK_CHOICES = [
        (1, "Week 1"),
        (2, "Week 2"),
        (3, "Week 3"),
        (4, "Week 4"),
        (5, "Week 5"),
        (6, "Week 6"),
        (7, "Week 7"),
        (8, "Week 8"),
        (9, "Week 9"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True, choices=PERIOD_CHOICES)
    week = models.IntegerField(blank=True, null=True, choices=WEEK_CHOICES)

    def __str__(self):
        return self.title
