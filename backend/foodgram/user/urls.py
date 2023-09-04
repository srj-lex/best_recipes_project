from rest_framework.routers import SimpleRouter

from django.urls import include, path, re_path

from .views import FollowListViewSet, create_destroy_view


router = SimpleRouter()
router.register("users/subscriptions", FollowListViewSet, basename="follow")


urlpatterns = [
    re_path(r"users/(?P<user_id>\d+)/subscribe/", create_destroy_view),
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include("djoser.urls")),
]
