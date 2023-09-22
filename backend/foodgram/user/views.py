from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from user.paginations import UserListPagination

from .models import Follow
from .serializers import FollowCreateDestroySerializer, FollowListSerializer


User = get_user_model()


class FollowAPI(APIView):
    """
    Класс создания и удаления объекта 'Подписка'.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user_id):
        request.data["author"] = user_id
        request.data["follower"] = request.user.id

        serializer = FollowCreateDestroySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED, data=serializer.data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        request.data["author"] = user_id
        request.data["follower"] = request.user.id

        author = get_object_or_404(User, pk=user_id)
        instance = get_object_or_404(
            Follow, author=author, follower=request.user
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для отображения списка подписок.
    """

    serializer_class = FollowListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UserListPagination

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        recipes_limit = self.request.GET.get("recipes_limit")
        if recipes_limit:
            context["recipes_limit"] = int(recipes_limit)

        return context
