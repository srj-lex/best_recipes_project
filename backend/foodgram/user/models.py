from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class Follow(models.Model):
    """
    Описывает поля объекта 'Подписка'.
    """

    author = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="author",
    )

    follower = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="follower",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "follower"], name="uq_author_follower"
            )
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self) -> str:
        return f"{self.follower.username} подписан на {self.author.username}"


class CustomUser(AbstractUser):
    """
    Дополняет базовую абстрактную модель пользователя.
    """

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=(validate_username,),
        verbose_name="Псевдоним пользователя",
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        max_length=254,
        blank=False,
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=150, blank=False
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, blank=False
    )
    password = models.CharField(
        verbose_name="Пароль", max_length=150, blank=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
