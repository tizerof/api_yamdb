import re
import uuid

from django.core.mail import send_mail
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMIN_EMAIL

from .models import User, UserConfirmation
from .permissions import IsAdmin
from .serializer import (UserConfirmationSerializer, UserJWTSerializer,
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
        super().create(request, *args, **kwargs)
        return Response('Проверьте вашу почту')

    def perform_create(self, serializer):
        code = str(uuid.uuid4())
        serializer.save(confirmation_code=code)
        send_mail(
            'authentication',
            f'{code}',
            ADMIN_EMAIL,
            [f'{serializer.validated_data.get("email")}'],
            fail_silently=False,
        )


class SendJWTViewSet(mixins.CreateModelMixin,
                     GenericViewSet):
    """
    Создаёт новый аккаунт, даёт токен для него и удаляет
    объект UserConfirmation.
    """
    queryset = User.objects.all()
    serializer_class = UserJWTSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = serializer.validate_confirmation(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = data.get('email')
        self.perform_create(serializer, email)
        user = User.objects.filter(email=email).first()
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token), })

    def perform_create(self, serializer, email):
        default_username = re.sub('[@.!?#]', '', email)
        serializer.save(username=default_username)


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с моделью User
    """
    queryset = User.objects.all().order_by('id')
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
        return Response(serializer.data)
