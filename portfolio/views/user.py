from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import User
from portfolio.serializers import UserSerializer, UserCreateSerializer, UserResponseWithTokenSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, extend_schema_view
from core.permissions import IsSelfOrAdmin

@extend_schema_view(
    list=extend_schema(tags=["Users"]),
    retrieve=extend_schema(tags=["Users"]),
    create=extend_schema(tags=["Users"]),
    update=extend_schema(tags=["Users"]),
    partial_update=extend_schema(tags=["Users"]),
    destroy=extend_schema(tags=["Users"]),
    me=extend_schema(tags=["Users"]),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD for User:
    - list: admin only
    - retrieve: admin or self
    - create: registration (AllowAny) — return tokens
    - update/partial_update/destroy: self or admin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_permissions(self):
        # Для создания (регистрация) — AllowAny
        if self.action == 'create':
            return [AllowAny()]
        # Для списка — только админ
        if self.action == 'list':
            return [IsAdminUser()]
        # Для других действий — применяем IsSelfOrAdmin + аутентификацию
        return [IsSelfOrAdmin()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        """Регистрация: создаём пользователя и возвращаем refresh/access + данные."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        resp = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(resp, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def me(self, request):
        """GET /api/users/me/ — информация по текущему пользователю"""
        user = request.user
        if not user or not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user)
        return Response(serializer.data)
