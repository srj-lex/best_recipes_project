from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingridient(models.Model):
    """
    Описывает таблицу ингридиентов.
    """

    name = models.CharField(
        verbose_name="Название", max_length=200, blank=False
    )
    measurement_unit = models.CharField(
        verbose_name="Единицы измерения", max_length=30, blank=False
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Описывает таблицу тегов для рецептов.
    """

    name = models.CharField(
        verbose_name="Название", max_length=150, blank=False, unique=True
    )
    color = models.CharField(
        verbose_name="Цвет", max_length=24, blank=False, unique=True
    )
    slug = models.SlugField(verbose_name="Слаг", blank=False, unique=True)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Описывает таблицу рецептов.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="recipes",
        blank=False,
        verbose_name="Автор",
    )
    name = models.CharField(
        verbose_name="Название", max_length=150, blank=False
    )
    image = models.ImageField(upload_to=None, default=None)
    description = models.CharField(
        verbose_name="Описание", max_length=400, blank=False
    )
    ingridients = models.ManyToManyField(
        Ingridient, through="IngridientsForRecipe"
    )
    tags = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT,
        related_name="recipes",
        blank=False,
        verbose_name="Тэг",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления", blank=False
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class IngridientsForRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingridient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
