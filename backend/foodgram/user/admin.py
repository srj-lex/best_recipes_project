from typing import Any

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import Follow


User = get_user_model()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Конфигурация модели Follow для админки.
    """

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return (
            super().get_queryset(request).select_related("author", "follower")
        )


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Конфигурация модели CustomUser для админки:
    добавлены фильтры списка
    по email и имени пользователя;
    """

    list_filter = ("email", "username")
