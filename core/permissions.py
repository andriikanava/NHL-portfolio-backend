from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class CanViewProject(BasePermission):
    """
    object-level: админ может всё, visitor — только если в allowed_users.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated or not user.verify:
            return False
        if user.is_staff or not obj.private:
            return True
        return obj.allowed_users.filter(id=user.id).exists()


class CanViewFile(BasePermission):
    """
    object-level для UploadedFile:
    админ — всё, visitor — если он в allowed_users проекта файла.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated or not user.verify:
            return False
        if user.is_staff or not obj.project.private:
            return True
        return obj.project.allowed_users.filter(id=user.id).exists()


class IsSelfOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or obj == request.user)