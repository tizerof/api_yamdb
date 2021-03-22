import uuid

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.mail import send_mail

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile, UserConfirmation
from .serializer import ProfileSerializer


class EmailConfirmApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        """
        Получает email, а в ответ создаёт и записывает в базу
        код подтверждения, и отправляет его пользователю на почту.
        """
        Email = request.data['email']
        token = str(uuid.uuid4())
        try:
            UserConfirmation.objects.create(email=Email,
                                            confirmation_code=token)
        except IntegrityError:
            return Response('Почта уже зарегистрирована',
                            status=status.HTTP_403_FORBIDDEN)
        send_mail(
            'authentication',
            f'{token}',
            'from@example.com',
            [f'{Email}'],
            fail_silently=False,
        )
        return Response('Проверьте вашу почту')


class SendJWTApiView(APIView):
    """
    Получает на вход почту и код подтверждения
    Проверяет правильность кода, если всё верно,
    Генерирует токен и возвращает его пользователю.
    """
    permission_classes = [AllowAny, ]

    def post(self, request):
        Email = request.data['email']
        confirmation_code = request.data['confirmation_code']
        UserObj = get_object_or_404(UserConfirmation, email=Email)
        if UserObj.confirmation_code != confirmation_code:
            return Response('Неверный код подтверждения',
                            status=status.HTTP_403_FORBIDDEN)

        """создаём объект пользователя"""
        user = User.objects.create_user(Email)
        user.email = Email
        user.password = confirmation_code
        user.save()

        """создаём профиль пользователя"""
        Profile.objects.create(username=Email,
                               email=Email)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
        })


class UsersModelViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


'''
Нужно всё делать с кастомной моделью, не трогать стандартную. 
Переделай регистрацию, чтобы на вход принимались все поля кастомной модели

'''