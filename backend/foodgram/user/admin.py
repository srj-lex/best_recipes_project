from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    """
    для модели пользователей добавить фильтр
    списка по email и имени пользователя;
    """

    list_filter = ("email", "username")


admin.site.register(CustomUser, UserAdmin)
