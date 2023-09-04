from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, permissions, viewsets

from .models import Ingridient, Recipe, Tag
from .serializers import IngridientSerializer, RecipeSerializer, TagSerializer


class TagViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngridientViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "is_favorited",
        "is_in_shopping_cart",
        "author",
        "tags",
    )
    pagination_class = pagination.LimitOffsetPagination
