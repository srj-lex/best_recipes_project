from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TagViewset, IngridientViewset

router = SimpleRouter()
router.register('tags', TagViewset)
router.register('ingridients', IngridientViewset)


urlpatterns = [
    path('', include(router.urls)),
]
