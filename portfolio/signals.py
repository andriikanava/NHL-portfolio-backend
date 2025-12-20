from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Project

User = get_user_model()

@receiver(post_save, sender=Project)
def add_all_users_on_project_create(sender, instance: Project, created: bool, **kwargs):
    if not created:
        return

    # Если private=True — НЕ добавляем никого по дефолту (логично для приватности)
    if instance.private:
        return

    instance.allowed_users.set(User.objects.all())
