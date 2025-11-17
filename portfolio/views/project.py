from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from core.models import Project
from portfolio.serializers import ProjectSerializer
from django.shortcuts import get_object_or_404


class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Полный CRUD для проекта с ручной логикой.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # Пример кастомной логики при создании
    def create(self, request, *args, **kwargs):
        data = request.data
        # Пример: запретить пустой title
        if not data.get('title'):
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Пример кастомной логики при обновлении
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

    # Пример кастомной логики при удалении
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
