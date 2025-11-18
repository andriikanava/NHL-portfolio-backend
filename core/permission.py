from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Разрешаем редактировать/удалять только самому пользователю (owner) или admin.
    Чтение допускается всем, если view.permission_classes это позволяет.
    """
    def has_object_permission(self, request, view, obj):
        # Админ может всё
        if request.user and request.user.is_staff:
            return True
        # Для безопасных методов — разрешаем всем (читай view defaults)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для остальных — только владелец
        return obj.id == getattr(request.user, 'id', None)
