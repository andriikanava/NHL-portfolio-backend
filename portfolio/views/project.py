from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from core.models import Project
from portfolio.serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdmin, CanViewProject
from django.db.models import Q

@extend_schema_view(
    list=extend_schema(tags=["Projects"]),
    retrieve=extend_schema(tags=["Projects"]),
    create=extend_schema(tags=["Projects"]),
    update=extend_schema(tags=["Projects"]),
    partial_update=extend_schema(tags=["Projects"]),
    destroy=extend_schema(tags=["Projects"]),
)
class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Project CRUD
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        qs = Project.objects.all()
        user = self.request.user

        # гость -> только публичные
        if not user.is_authenticated:
            return qs.filter(private=False)

        # staff -> всё
        if user.is_staff:
            return qs

        # обычный юзер -> public + разрешённые
        return qs.filter(Q(private=False) | Q(allowed_users=user)).distinct()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [CanViewProject()]
        return [IsAdmin()]

    def create(self, request, *args, **kwargs):
        data = request.data
        if not data.get('title'):
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

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
