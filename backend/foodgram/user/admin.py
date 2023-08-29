from django.contrib import admin

from .models import CustomUser, Follow


class UserAdmin(admin.ModelAdmin):
    """
    Конфигурация модели User для админки:
    добавлены фильтры
    списка по email и имени пользователя;
    """

    list_filter = ("email", "username")


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Follow)
