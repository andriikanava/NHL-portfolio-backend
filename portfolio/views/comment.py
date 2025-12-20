from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from core.models import Comment
from portfolio.serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from core.permissions import IsAdmin

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


@extend_schema_view(
    list=extend_schema(tags=["Comments"]),
    retrieve=extend_schema(tags=["Comments"]),
    create=extend_schema(tags=["Comments"]),
    update=extend_schema(tags=["Comments"]),
    partial_update=extend_schema(tags=["Comments"]),
    destroy=extend_schema(tags=["Comments"]),
)
class CommentViewSet(
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
    serializer_class = CommentSerializer
    def get_queryset(self):
        # админ видит все комментарии
        return Comment.objects.select_related("project", "user")

    def get_permissions(self):
        return [IsAdmin()]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
