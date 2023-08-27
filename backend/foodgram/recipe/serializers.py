from rest_framework import serializers

from .models import Tag, Ingridient


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.
    """

    class Meta:
        model = Tag
        fields = ("pk", "name", "color", "slug")


class IngridientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.
    """

    class Meta:
        model = Ingridient
        fields = ("pk", "name", "measurement_unit")
