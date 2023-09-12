from django.contrib import admin

from .models import Recipe, Tag, Ingredient, IngredientForRecipe, Favorite, ShoppingCart


class IngredientForRecipeInline(admin.TabularInline):
    model = IngredientForRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    """
    для модели рецептов:
        - в списке рецептов вывести название и имя автора рецепта; X
        - добавить фильтры по автору, названию рецепта, тегам; X
        - на странице рецепта вывести общее число добавлений этого рецепта в избранное; ?
    """

    list_display = ("name", "author")
    list_filter = ("author", "name", "tags")
    inlines = (IngredientForRecipeInline,)


class IngredientAdmin(admin.ModelAdmin):
    """
    для модели ингредиентов:
        - в список вывести название ингредиента и единицы измерения; X
        - добавить фильтр по названию. X
    """

    list_filter = ("name",)
    list_display = ("name", "measurement_unit")


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
