import base64

from rest_framework import serializers, validators

from django.core.files.base import ContentFile

from user.serializers import UserSerializer

from .models import Ingredient, Recipe, Tag, IngredientForRecipe, Favorite, ShoppingCart


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.
    """

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ingredient.
    """

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


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


class IngredientsForRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения связи ингредиент-рецепт.
    """

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientForRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения модели Recipe.
    """

    tags = TagSerializer(
        many=True,
    )
    author = UserSerializer()
    ingredients = IngredientsForRecipeSerializer(
        many=True, source="ingredientforrecipe_set"
    )
    # image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            # "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return Favorite.objects.filter(
            recipe=obj, user=current_user).exists()

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            recipe=obj, user=current_user).exists()


class IngredientForRecipeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания связи ингредиент-рецепт.
    """

    id = serializers.PrimaryKeyRelatedField(
        source="ingredients", queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientForRecipe
        fields = ("id", "amount")


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания рецепта.
    """

    ingredients = IngredientForRecipeCreateSerializer(
        many=True,
    )
    # image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "ingredients",
            "name",
            # "image",
            "text",
            "cooking_time",
        )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tag = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tag)

        for ingredient in ingredients:
            IngredientForRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient["ingredients"],
                amount=ingredient["amount"],
            )
        return recipe

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        # instance.image = validated_data.get('image', instance.image)
        if "tags" in validated_data:
            tag = validated_data.pop("tags")
            instance.tags.set(tag)

        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            for ingredient in ingredients:
                IngredientForRecipe.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient["ingredients"],
                    defaults={"amount": ingredient["amount"]},
                )

        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор добавления рецептов в избранное.
    """

    validators = [
        validators.UniqueTogetherValidator(
            queryset=Favorite.objects.all(),
            fields=("user", "recipe"),
            message="Рецепт уже добвален в избранное!"
        )
    ]

    class Meta:
        model = Favorite
        fields = (
            "user",
            "recipe"
        )


class MinRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор рецепта с минимальным колчичеством полей.
    """

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            # "image",
            "cooking_time"
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор добавления ингридиентов из рецепта в корзину.
    """

    validators = [
        validators.UniqueTogetherValidator(
            queryset=ShoppingCart.objects.all(),
            fields=("user", "recipe"),
            message="Рецепт уже добвален в корзину!"
        )
    ]

    class Meta:
        model = ShoppingCart
        fields = (
            "user",
            "recipe"
        )
