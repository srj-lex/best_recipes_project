import re

from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.forms import ValidationError

from .models import Follow
from recipe.models import Recipe


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes"
        )

    def get_is_subscribed(self, obj):
        if self.context:
            current_user = self.context.get("request").user
            if current_user.is_anonymous or current_user == obj:
                return False
            return Follow.objects.filter(
                author=current_user, follower=obj
            ).exists()
        return False


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


class MinRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор рецепта с минимальным колчичеством полей.
    """

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class FollowListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения подписок текущего пользователя.
    """

    email = serializers.EmailField(source="author.email") 
    id = serializers.IntegerField(source="author.id")
    username = serializers.CharField(source="author.username")
    first_name = serializers.CharField(source="author.first_name")
    last_name = serializers.CharField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ("email", "id", "username", "first_name", "last_name", "is_subscribed", "recipes", "recipes_count")

    def get_is_subscribed(self, obj):
        if self.context:
            current_user = self.context.get("request").user
            if current_user.is_anonymous or current_user == obj.author:
                return False
            return Follow.objects.filter(
                follower=current_user,
            ).exists()
        return False

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.author)
        serializer = MinRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


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
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
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
        username = data["username"]

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f"Пользователь с таким username — {username} — уже существует."
            )

        return data

    def to_representation(self, instance):
        serializer = UserSerializer(instance)
        return serializer.data
