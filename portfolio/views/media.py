from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from core.models import UploadedFile
from portfolio.serializers import UploadedFileSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdmin, CanViewFile
from django.db.models import Q

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


@extend_schema_view(
    list=extend_schema(tags=["Media"]),
    retrieve=extend_schema(tags=["Media"]),
    create=extend_schema(tags=["Media"]),
    destroy=extend_schema(tags=["Media"]),
)
class MediaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Comments CRUD
    """

    serializer_class = UploadedFileSerializer


    def get_queryset(self):
        user = self.request.user
        qs = UploadedFile.objects.select_related("project")

        project_id = self.request.query_params.get("project")
        if project_id:
            qs = qs.filter(project_id=project_id)

        # ✅ Гость: видит только файлы публичных проектов
        if not user.is_authenticated:
            return qs.filter(project__private=False)

        # ✅ Если ты хочешь требовать verify — делай это тут
        if not getattr(user, "verify", False):
            # можно разрешить только public, а private запретить
            return qs.filter(project__private=False)

        # ✅ Админ: видит всё
        if user.is_staff:
            return qs

        # ✅ Обычный юзер: public + private где он в allowed_users
        return qs.filter(Q(project__private=False) | Q(project__allowed_users=user)).distinct()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [CanViewFile()]
        return [IsAdmin()]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
