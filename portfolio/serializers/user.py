from rest_framework import serializers
from core.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода user (без пароля)."""
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_active', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'is_staff', 'is_active', 'date_joined')


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации / создания пользователя."""
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserResponseWithTokenSerializer(serializers.ModelSerializer):
    """Возвращаем пользователя + access/refresh после регистрации."""
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'refresh', 'access')
