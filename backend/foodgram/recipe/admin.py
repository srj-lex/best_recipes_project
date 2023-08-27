from django.contrib import admin


from .models import Ingridient, Tag, Recipe


class RecipeAdmin(admin.ModelAdmin):
    """
    для модели рецептов:
        - в списке рецептов вывести название и имя автора рецепта; X
        - добавить фильтры по автору, названию рецепта, тегам; X
        - на странице рецепта вывести общее число добавлений этого рецепта в избранное; ?
    """

    list_display = ("name", "author")
    list_filter = ("author", "name", "tag")


class IngridientAdmin(admin.ModelAdmin):
    """
    для модели ингредиентов:
        - в список вывести название ингредиента и единицы измерения; ?
        - добавить фильтр по названию. X
    """

    list_filter = ("name", )


admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
