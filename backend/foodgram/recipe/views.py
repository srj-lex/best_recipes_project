from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import json, csv

from .models import Ingredient, Recipe, Tag, Favorite, ShoppingCart, IngredientForRecipe
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    MinRecipeSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)
from user.paginations import UserListPagination
from .filters import RecipeFilter
from user.permissions import RecipeUserPermission


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
            "ingredientforrecipe_set__ingredient", "tags"
        ).all()
        return recipes

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ("create", "partial_update"):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=("post", "delete"),)
    def favorite(self, request, pk):
        """
        Обрабатывает создание и удаление записей
        в модели Favorite.
        """
        serializer = FavoriteSerializer(
            data={"user": request.user.id, "recipe": pk})

        if request.method == "POST":
            serializer.is_valid(raise_exception=True)
            Favorite.objects.get_or_create(
                **serializer.validated_data
            )
            return Response(
                status=status.HTTP_201_CREATED,
                data=MinRecipeSerializer(
                    serializer.validated_data["recipe"]).data
            )

        recipe = get_object_or_404(Recipe, pk=pk)
        obj = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
            )
        if not obj:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Такого рецепта нет в избранном!"}
                )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=("post", "delete"),)
    def shopping_cart(self, request, pk):
        """
        Обрабатывает создание и удаление записей
        в модели ShoppingCart.
        """
        serializer = ShoppingCartSerializer(
            data={"user": request.user.id, "recipe": pk})

        if request.method == "POST":
            serializer.is_valid(raise_exception=True)
            ShoppingCart.objects.get_or_create(
                **serializer.validated_data
            )
            return Response(
                status=status.HTTP_201_CREATED,
                data=MinRecipeSerializer(
                    serializer.validated_data["recipe"]).data
            )

        recipe = get_object_or_404(Recipe, pk=pk)
        obj = ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe
            )
        if not obj:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": "Такого рецепта нет в корзине!"}
                )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=("get", ))
    def download_shopping_cart(self, request):
        """
        Обрабатывает выгрузку содержимого корзины в файл.
        """
        current_user = request.user

        res = (
            IngredientForRecipe.objects
            .filter(recipe__shoppingcart__user=current_user)
            .values("ingredient")
            .annotate(total_amount=Sum("amount"))
            .values_list("ingredient__name", "total_amount",
                         "ingredient__measurement_unit")
        )

        response = HttpResponse(
            content_type="text/csv",
            status=status.HTTP_200_OK
            )
        data = list(res)
        columns_name = ('название', "количество", 'единица измерения')
        writer = csv.writer(response)
        writer.writerow(columns_name)                 # запись заголовков
        for row in data:                         # запись строк
            writer.writerow(row)

        return response
