from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Follow
from .serializers import FollowCreateDestroySerializer, FollowListSerializer
from .paginations import UserListPagination


User = get_user_model()


@api_view(["POST", "DELETE"])
def create_destroy_view(request, user_id):
    """
    Функция создания и удаления объекта 'Подписка'.
    """
    request.data["author"] = user_id
    request.data["follower"] = request.user.id

    if request.method == "POST":
        serializer = FollowCreateDestroySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    author = get_object_or_404(User, pk=user_id)
    instance = get_object_or_404(Follow, author=author, follower=request.user)
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
