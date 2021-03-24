import uuid

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework import viewsets, mixins, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserConfirmation, User
from .permissions import IsAdminOrReadOnly
from .serializer import UserSerializer, UserConfirmationSerializer, UsersSerializer, SpecificUserSerializer


class EmailConfirmationViewSet(mixins.CreateModelMixin,
                               GenericViewSet):
    """
    Получает на вход email в body,
    сериализуент объект, генерирует код подтверждения,
    сохраняет почту вместе с кодом в бд,
    отправляет письмо с кодом подтверждения на почту
    """
    queryset = UserConfirmation.objects.all()
    serializer_class = UserConfirmationSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('Проверьте вашу почту')

    def perform_create(self, serializer):
        code = str(uuid.uuid4())
        serializer.save(confirmation_code=code)
        send_mail(
            'authentication',
            f'{code}',
            'from@example.com',
            [f'{self.request.POST.get("email")}'],
            fail_silently=False,
        )


class sendJWTViewSet(mixins.CreateModelMixin,
                     GenericViewSet):
    """
    Получает на вход email и confirmation_code в body,
    сериализует объект, проверяет валидность кода,
    создаёт пользователя, возвращает токен пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = get_object_or_404(User, email=request.POST.get('email'))
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
        })

    def perform_create(self, serializer):
        confirmation_code = self.request.POST.get('confirmation_code')
        serializer.save(password=confirmation_code)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Возвразщает список всех пользователей,
    создаёт нового пользователя
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = [filters.SearchFilter]
    search_fields = "username"

    def perform_create(self, serializer):
        serializer.save(password=str(uuid.uuid4()))


class SpecificUserViewSet(viewsets.ModelViewSet):
    serializer_class = SpecificUserSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    http_method_names = ('delete', 'get', 'patch')
    lookup_field = 'username'
    pagination_class = None

    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs.get('username'))
        return user
