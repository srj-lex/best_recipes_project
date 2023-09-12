from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    """
    Описывает таблицу ингредиентов.
    """

    name = models.CharField(
        verbose_name="Название", max_length=200, blank=False
    )
    measurement_unit = models.CharField(
        verbose_name="Единицы измерения", max_length=30, blank=False
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
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
        on_delete=models.CASCADE,
        related_name="recipes",
        blank=False,
        verbose_name="Автор",
    )
    name = models.CharField(
        verbose_name="Название", max_length=150, blank=False
    )
    # image = models.ImageField(
    #     verbose_name="Изображение",
    #     upload_to=None,
    #     default=None
    #     )
    text = models.TextField(
        verbose_name="Описание", max_length=500, blank=False
    )
    tags = models.ManyToManyField(Tag, verbose_name="Тэг")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientForRecipe",
        through_fields=("recipe", "ingredient"),
        verbose_name="Ингредиент",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления", blank=False
    )
    is_favorited = models.ManyToManyField("Favorite", verbose_name="Избранное", related_name="is_favorite")
    is_in_shopping_cart = models.ManyToManyField("ShoppingCart", verbose_name="Корзина", related_name="is_in_shopping_cart")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    """
    Таблица отношения М2М для Рецепта и Ингредиента.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.recipe} - {self.ingredient} - {self.amount}"


class Favorite(models.Model):
    """
    Таблица с записями, отображающими добавление
    пользователем рецепта в избранное.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="uq_user_recipe"
            )
        ]

        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self) -> str:
        return f"{self.user} - {self.recipe}"


class ShoppingCart(models.Model):
    """
    Таблица с записями, отображающими добавление
    рецепта в корзину пользователя.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="uq_shopping_cart"
            )
        ]

        verbose_name = "Корзина покупок"
        verbose_name_plural = "Корзина покупок"

    def __str__(self) -> str:
        return f"{self.user} - {self.recipe}"
