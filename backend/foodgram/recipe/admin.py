from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import (
    Favorite,
    Ingredient,
    IngredientForRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


class IngredientForRecipeInline(admin.TabularInline):
    model = IngredientForRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Настройки админки для модели рецептов.
    """

    readonly_fields = ("recipe_fav_count",)

    list_display = ("name", "author")
    list_filter = ("author", "tags")
    search_fields = ("name",)
    inlines = (IngredientForRecipeInline,)

    @admin.display(description="Число добавлений в избранное")
    def recipe_fav_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return (
            super()
            .get_queryset(request)
            .select_related("author")
            .prefetch_related("tags", "ingredients")
        )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Настройки админки для модели ингредиентов.
    """

    search_fields = ("name",)
    list_display = ("name", "measurement_unit")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Настройки админки для модели тегов.
    """

    search_fields = ("name",)
    list_display = ("name", "color")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Настройки админки для модели избранное.
    """

    list_filter = ("user", "recipe")
    list_display = ("user", "recipe")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related("user", "recipe")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Настройки админки для модели корзины покупок.
    """

    list_filter = ("user", "recipe")
    list_display = ("user", "recipe")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related("user", "recipe")
