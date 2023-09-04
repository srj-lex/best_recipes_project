from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import IngridientViewset, RecipeViewSet, TagViewset


router = SimpleRouter()
router.register("tags", TagViewset)
router.register("ingridients", IngridientViewset)
router.register("recipes", RecipeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
