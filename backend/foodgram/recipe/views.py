import csv

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Sum
from django.db.models.query import QuerySet
from django.http import HttpResponse

from user.paginations import UserListPagination
from user.permissions import RecipeUserPermission

from .filters import RecipeFilter
from .models import (
    Favorite,
    Ingredient,
    IngredientForRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    MinRecipeSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)


class TagViewset(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет модели Tag.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientViewset(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет модели Ingredient.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Recipe.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (RecipeUserPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = UserListPagination
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            "recipe_m2m__ingredient", "tags"
        ).select_related("author")
        return recipes

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ("create", "partial_update"):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk):
        """
        Обрабатывает создание и удаление записей
        в модели Favorite.
        """
        serializer = FavoriteSerializer(
            data={"user": request.user.id, "recipe": pk}
        )

        if request.method == "POST":
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=MinRecipeSerializer(
                    serializer.validated_data["recipe"]
                ).data,
            )

        obj = Favorite.objects.filter(user=request.user, recipe=pk)
        if not obj:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Такого рецепта нет в избранном!"},
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        """
        Обрабатывает создание и удаление записей
        в модели ShoppingCart.
        """
        serializer = ShoppingCartSerializer(
            data={"user": request.user.id, "recipe": pk}
        )

        if request.method == "POST":
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=MinRecipeSerializer(
                    serializer.validated_data["recipe"]
                ).data,
            )

        obj = ShoppingCart.objects.filter(user=request.user, recipe=pk)
        if not obj:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Такого рецепта нет в корзине!"},
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @classmethod
    def create_shopping_list(cls, cart_obj: QuerySet) -> HttpResponse:
        response = HttpResponse(
            content_type="text/csv", status=status.HTTP_200_OK
        )
        columns_name = ("название", "количество", "единица измерения")
        writer = csv.writer(response)
        writer.writerow(columns_name)
        for row in cart_obj:
            writer.writerow(row)

        return response

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        """
        Обрабатывает выгрузку содержимого корзины в файл.
        """
        cart_obj = (
            IngredientForRecipe.objects.filter(
                recipe__recipe_shopcart__user=request.user
            )
            .values("ingredient")
            .annotate(total_amount=Sum("amount"))
            .values_list(
                "ingredient__name",
                "total_amount",
                "ingredient__measurement_unit",
            )
        )

        return self.create_shopping_list(cart_obj)
