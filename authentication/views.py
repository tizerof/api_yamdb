import secrets

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import Users, UserConfirmation
from rest_framework.permissions import AllowAny


class EmailApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        """
        Нужно проверять, чтобы почта была новая
        """
        Email = request.data['Email']
        token = secrets.token_hex
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
