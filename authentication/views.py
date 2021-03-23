import uuid

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserConfirmation, User
from .serializer import UserSerializer, UserConfirmationSerializer


class EmailConfirmationViewSet(viewsets.ModelViewSet):
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


class sendJWTModelViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    """
    Получает на вход email и confirmation_code в body
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
        Email = self.request.POST.get('email')
        confirmation_code = self.request.data['confirmation_code']
        serializer.save(password=confirmation_code,
                        username=Email)


class UsersModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
