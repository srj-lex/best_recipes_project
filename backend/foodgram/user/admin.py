from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import CustomUser, Follow


class FollowAdmin(admin.ModelAdmin):
    """
    Конфигурация модели Follow для админки.
    """

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Follow.objects.select_related("author", "follower")


class CustomUserAdmin(UserAdmin):
    """
    Конфигурация модели CustomUser для админки:
    добавлены фильтры списка
    по email и имени пользователя;
    """

    list_filter = ("email", "username")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)
