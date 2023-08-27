
# from rest_framework.decorators import action, api_view
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from rest_framework import mixins, viewsets

# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404


# from .serializers import UserSerializer, UserCreateSerializer, FollowSerializer
# from .models import Follow


# User = get_user_model()


# class FollowViewSet(mixins.ListModelMixin,
#                     viewsets.GenericViewSet):
#     """
#     Вьюсет для работы с эндпоинтом users/subscriptions/
#     """
#     serializer_class = FollowSerializer
#     queryset = User.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)


# class UserViewSet(
#         mixins.CreateModelMixin,
#         mixins.ListModelMixin,
#         mixins.RetrieveModelMixin,
#         viewsets.GenericViewSet
#         ):
#     """
#     Вьюсет для работы с эндпоинтом users/
#     """

#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return UserCreateSerializer
#         return UserSerializer

#     @action(
#         methods=("get",),
#         detail=False,
#         url_path="me",
#         permission_classes=(permissions.IsAuthenticated,),
#     )
#     def user_detail_view(self, request):
#         """
#         Функция для работы с эндпоинтом user/me/.
#         """
#         user_data = get_object_or_404(User, pk=request.user.pk)
#         serializer = UserSerializer(user_data, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)
