from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.permissions import IsOwner
from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer


class UserListAPIView(generics.ListAPIView):
    """ Класс для вывода списка пользователей """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ Класс для вывода одного пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Класс для изменения пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    """ Класс для удаления пользователя """

    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsOwner]


class UsersRegistrationView(generics.CreateAPIView):
    """
    Сериализатор для регистрации нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)
