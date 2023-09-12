from rest_framework.permissions import SAFE_METHODS, BasePermission


class RecipeUserPermission(BasePermission):
    """
    Разрешения для доступа к рецептам.
    """

    message = "Изменение чужого контента запрещено!"

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
