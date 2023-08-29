from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ("user", "Пользователь"),
    ("admin", "Администратор"),
)


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
        return self.author.username


class CustomUser(AbstractUser):
    """
    Дополняет базовую абстрактную модель пользователя.
    """

    email = models.EmailField(verbose_name="Электронная почта", max_length=254, blank=False)
    first_name = models.CharField(verbose_name="Имя", max_length=150, blank=False)
    last_name = models.CharField(verbose_name="Фамилия", max_length=150, blank=False)
    password = models.CharField(verbose_name="Пароль", max_length=150, blank=False)
    is_subscribed = models.BooleanField(verbose_name="Подписчик", default=False)
    role = models.CharField(
        max_length=16, choices=CHOICES, default="user", verbose_name="Роль"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
