from django.db import models

from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # время создания
    updated_at = models.DateTimeField(auto_now=True)      # время изменения

    class Meta:
        abstract = True  # Django не создаст отдельную таблицу для BaseModel
