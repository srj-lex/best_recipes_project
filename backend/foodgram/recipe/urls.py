from rest_framework.routers import DefaultRouter

from django.urls import include, path, re_path

from user.views import FollowAPI, FollowListViewSet

from .views import IngredientViewset, RecipeViewSet, TagViewset


router = DefaultRouter()
router.register("users/subscriptions", FollowListViewSet, basename="follow")
router.register("tags", TagViewset)
router.register("ingredients", IngredientViewset)
router.register("recipes", RecipeViewSet)


urlpatterns = [
    re_path(r"users/(?P<user_id>\d+)/subscribe/", FollowAPI.as_view()),
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include("djoser.urls")),
]
