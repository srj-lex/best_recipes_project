from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Ingridient(models.Model):
    """
    Описывает таблицу ингридиентов.
    """

    name = models.CharField(verbose_name="Название", max_length=200, blank=False)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество", blank=False)
    measurement_unit = models.CharField(verbose_name="Единицы измерения", max_length=30, blank=False)

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Описывает таблицу тегов для рецептов.
    """

    name = models.CharField(verbose_name="Название", max_length=150, blank=False, unique=True)
    color = models.CharField(verbose_name="Цвет", max_length=24, blank=False, unique=True)
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

    # Автор публикации (пользователь).
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="recipes",
        blank=False,
        verbose_name="Автор",
    )
    # Название.
    name = models.CharField(verbose_name="Название", max_length=150, blank=False)
    # Картинка.
    image = models.ImageField(
        upload_to=None,
        default=None
        )
    # Текстовое описание.
    description = models.CharField(verbose_name="Описание", max_length=400, blank=False)
    # Ингредиенты — продукты для приготовления блюда по рецепту.
    # Множественное поле с выбором из предустановленного списка
    # и с указанием количества и единицы измерения.
    ingridients = models.ForeignKey(
        Ingridient,
        on_delete=models.PROTECT,
        related_name="recipes",
        blank=False,
        verbose_name="Ингридиенты"
    )

    # Тег. Можно установить несколько тегов на один рецепт.
    tag = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT,
        related_name="recipes",
        blank=False,
        verbose_name="Тэг"
    )
    # Время приготовления в минутах.
    time = models.PositiveSmallIntegerField(verbose_name="Время приготовления", blank=False)
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name
