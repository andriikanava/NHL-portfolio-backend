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
        qs = UploadedFile.objects.select_related("project")
        user = self.request.user

        if not user.is_authenticated:
            return qs.none()

        if user.is_staff:
            return qs

        return qs.filter(project__allowed_users=user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), CanViewFile()]
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
