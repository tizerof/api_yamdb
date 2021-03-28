import re
import uuid

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserConfirmation, User
from .permissions import IsAdmin
from .serializer import (UserJWTSerializer, UserConfirmationSerializer,
                         UsersViewSetSerializer)


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
    В случае если к почте пользователя не привязан ни один аккаунт,
    создаёт новый, даёт токен для него и удаляет объект UserConfirmation.
    Если аккаунт уже имеется, то проверяет confirmation_code и
    обновляет токен для аккаунта, на который зарегистрирована почта.
    """
    queryset = User.objects.all()
    serializer_class = UserJWTSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        request_email = request.POST.get('email')
        request_code = request.POST.get('confirmation_code')

        """ Если пользователь регистрируется впервые, создаем ему аккаунт """
        try:
            user = User.objects.get(email=request_email)
        except User.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = get_object_or_404(User, email=request_email)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
            })

        try:
            confirm = UserConfirmation.objects.get(email=request_email)
        except UserConfirmation.DoesNotExist:
            raise ValidationError('Код подтверждения неверен')

        if confirm.confirmation_code != request_code:
            raise ValidationError('Код подтверждения неверен')

        confirm.delete()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
        })


class UsersViewSet(viewsets.ModelViewSet):
    """
    Возвразщает список всех пользователей,
    создаёт нового пользователя
    """
    queryset = User.objects.all()
    serializer_class = UsersViewSetSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = [filters.SearchFilter]
    search_fields = "username"
    lookup_field = "username"

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated, ])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
