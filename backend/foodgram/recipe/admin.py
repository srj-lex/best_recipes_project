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


class RecipeAdmin(admin.ModelAdmin):
    """
    Настройки админки для модели рецептов.
    """

    list_display = ("name", "author")
    list_filter = ("author", "name", "tags")
    inlines = (IngredientForRecipeInline,)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Recipe.objects.select_related("author").prefetch_related(
            "tags", "ingredients"
        )


class IngredientAdmin(admin.ModelAdmin):
    """
    Настройки админки для модели ингредиентов.
    """

    list_filter = ("name",)
    list_display = ("name", "measurement_unit")


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
