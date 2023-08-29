import re
from rest_framework import serializers
from django.forms import ValidationError
from django.contrib.auth import get_user_model

from .models import Follow


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.
    """

    class Meta:
        model = User
        fields = ("email", "pk", "username", "first_name", "last_name", "is_subscribed", "recipes")


class FollowCreateDestroySerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и удаления объекта 'Подписка'.
    """

    class Meta:
        model = Follow
        fields = ("author", "follower")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=[
                    "author",
                    "follower",
                ],
            )
        ]

    def validate(self, data):
        if data["author"] == data["follower"]:
            raise ValidationError(message="Нельзя подписаться на самого себя")
        return data


class FollowListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения подписок текущего пользователя.
    """

    author = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ("author", )


class UserCreateSerializer(serializers.Serializer):
    """
    Сериализатор для создания нового пользователя.
    """

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)
    password = serializers.CharField(required=True, max_length=150)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        password = validated_data["password"]

        user, _ = User.objects.get_or_create(
            email=email, username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user

    def validate_username(self, value):
        if not re.fullmatch(r"^[\w.@+-]+$", value):
            raise serializers.ValidationError(
                "В username используются недопустимые символы"
            )

        if value.lower() == "me":
            raise serializers.ValidationError("Укажите другой username")

        return value

    def validate(self, data):
        username = data['username']

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким username — {username} — уже существует.'
            )

        return data
