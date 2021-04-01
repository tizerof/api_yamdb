from django.core.validators import EmailValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, UserConfirmation


class UserConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UserConfirmation


class UserJWTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password', 'role', 'email',
                  'bio', 'first_name', 'last_name')
        model = User

        confirmation_code = serializers.CharField()

    def validate_code(self, raise_exception=False):
        email = self.context['request'].POST.get('email')
        user_obj = get_object_or_404(UserConfirmation, email=email)
        confirmation_code = self.context['request'].data['confirmation_code']
        if user_obj.confirmation_code != confirmation_code:
            raise ValidationError('Код подтверждения неверен')

        valid = super().is_valid(raise_exception=raise_exception)
        user_obj.delete()
        return valid

    def email_validation(self, value):
        validator = EmailValidator(message='Недопустимый формат почты',
                                   code=400)
        validator(value)
        return value

    def confirmation_validation(self, value):
        if len(value) == 36:
            return value
        raise ValueError('Недопустимый формат кода подтверждения')


class UsersViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password', 'role', 'email',
                  'bio', 'first_name', 'last_name', 'is_superuser')
        model = User
