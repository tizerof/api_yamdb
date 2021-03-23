import uuid

from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.mail import send_mail

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserConfirmation, User
from .serializer import UserSerializer


class EmailConfirmApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        """
        Получает email, а в ответ создаёт и записывает в базу
        код подтверждения, и отправляет его пользователю на почту.
        """
        Email = request.POST.get('email')

        confirmation_code = str(uuid.uuid4())
        try:
            UserConfirmation.objects.create(email=Email,
                                            confirmation_code=confirmation_code)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            'authentication',
            f'{confirmation_code}',
            'from@example.com',
            [f'{Email}'],
            fail_silently=False,
        )
        return Response('Проверьте вашу почту')


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
        Username = Email.split('@')[0]
        confirmation_code = self.request.data['confirmation_code']
        serializer.save(password=confirmation_code,
                        username=Username)


class UsersModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
