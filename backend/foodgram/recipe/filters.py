from django_filters import rest_framework as filters

from .models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """Фильтр выборки рецептов по определенным полям."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="get_is_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
        )

    def get_is_favorited(self, queryset, name, value):
        current_user = self.request.user
        if current_user.is_authenticated and value:
            return queryset.filter(recipe_favorite__user=current_user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        current_user = self.request.user
        if current_user.is_authenticated and value:
            return queryset.filter(recipe_shopcart__user=current_user)
        return queryset
