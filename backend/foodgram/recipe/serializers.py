import base64

from rest_framework import serializers

from django.core.files.base import ContentFile

from user.serializers import UserSerializer

from .models import Ingridient, IngridientsForRecipe, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.
    """

    class Meta:
        model = Tag
        fields = ("pk", "name", "color", "slug")


class IngridientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ingridient.
    """

    class Meta:
        model = Ingridient
        fields = ("pk", "name", "measurement_unit")


class IngridientsForRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели IngridientAmount.
    """

    class Meta:
        model = IngridientsForRecipe
        fields = (
            "ingridient",
            "amount",
        )


class Base64ImageField(serializers.ImageField):
    """
    Описание кастомного поля сериализатора для обработки изображений.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Recipe.
    """

    tags = TagSerializer(
        many=True,
    )
    author = UserSerializer()
    ingridients = IngridientSerializer(
        many=True,
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "pk",
            "tags",
            "author",
            "ingridients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "description",
            "cooking_time",
        )

    def create(self, validated_data):
        ingridients = validated_data.pop("ingridients")
        data = []
        for ingridient in ingridients:
            (
                current_ingridient,
                status,
            ) = IngridientAmount.objects.get_or_create(**ingridient)
            data.append(current_ingridient)

        print(data)
        # recipe = Recipe.objects.create(**validated_data, ingridients=data)
        # return recipe
