import re
import uuid

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework import viewsets, mixins, filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserConfirmation, User
from .permissions import IsAdmin
from .serializer import (UserJWTSerializer, UserConfirmationSerializer,
                         UsersViewSetSerializer, SpecificUserSerializer,
                         UserAPIViewSerializer)


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

    def perform_create(self, serializer):
        email = self.request.POST.get('email')
        default_username = re.sub('[@.!?#]', '', email)
        confirmation_code = self.request.POST.get('confirmation_code')
        serializer.save(password=confirmation_code,
                        username=default_username)


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

    def perform_create(self, serializer):
        serializer.save(password=str(uuid.uuid4()))


class SpecificUserViewSet(viewsets.ModelViewSet):
    """
    Возвращает данные одного пользователя по username,
    позволяет менять его поля [PATCH] или удалить объект
    """
    queryset = User.objects.all()
    serializer_class = SpecificUserSerializer
    permission_classes = [IsAdmin, ]
    http_method_names = ('delete', 'get', 'patch')
    lookup_field = 'username'
    pagination_class = None


class UserAPIView(APIView):
    """
    Возвращает данные поста пользователя при запросе к /users/me/
    Позволяет менять данные своего профиля
    """
    permission_classes = [IsAuthenticate]

    def get(self, request):
        username = request.user.username
        UserObj = User.objects.get(username=username)
        serializer = UserAPIViewSerializer(UserObj)
        return Response(serializer.data)

    def patch(self, request):
        username = request.user.username
        UserObj = User.objects.get(username=username)
        serializer = UserAPIViewSerializer(UserObj,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
