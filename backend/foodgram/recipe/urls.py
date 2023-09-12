from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import IngredientViewset, RecipeViewSet, TagViewset


router = SimpleRouter()
router.register("tags", TagViewset)
router.register("ingredients", IngredientViewset)
router.register("recipes", RecipeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
