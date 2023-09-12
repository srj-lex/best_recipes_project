from django_filters import rest_framework as filters

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    """Фильтр выборки рецептов по определенным полям."""

    tags = filters.CharFilter(field_name="tags__slug", lookup_expr="icontains")
    is_favorited = filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="get_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
        )

    def get_is_favorited(self, queryset, name, value):
        current_user = self.request.user
        if current_user.is_authenticated and value:
            return queryset.filter(favorite__user=current_user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        current_user = self.request.user
        if current_user.is_authenticated and value:
            return queryset.filter(shoppingcart__user=current_user)
        return queryset
