from rest_framework import viewsets

from .serializers import TagSerializer, IngridientSerializer
from .models import Tag, Ingridient


class TagViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngridientViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer
    pagination_class = None
