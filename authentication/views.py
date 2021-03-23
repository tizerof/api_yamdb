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
        Email = request.data['email']
        confirmation_code = str(uuid.uuid4())
        try:
            UserConfirmation.objects.create(email=Email,
                                            confirmation_code=confirmation_code)
        except IntegrityError:
            return Response('Почта уже зарегистрирована',
                            status=status.HTTP_403_FORBIDDEN)
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = get_object_or_404(User, email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
        })

    def perform_create(self, serializer):
        Email = self.request.data['email']
        confirmation_code = self.request.data['confirmation_code']
        UserObj = get_object_or_404(UserConfirmation, email=Email)
        if UserObj.confirmation_code != confirmation_code:
            return Response('Неверный код подтверждения',
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save(password=confirmation_code)


class UsersModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
