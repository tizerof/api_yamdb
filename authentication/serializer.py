from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, UserConfirmation


class UserConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UserConfirmation


class UserJWTSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()

    class Meta:
        fields = ('username', 'password', 'role', 'email',
                  'bio', 'first_name', 'last_name')
        model = User
        confirmation_code = serializers.CharField()

    def validate_confirmation(self, data):
        email = data.get('email')
        confirmation_code = data.get('confirmation_code')
        user_conf = UserConfirmation.objects.filter(
            email=email, confirmation_code=confirmation_code).first()
        if user_conf is None:
            raise ValidationError(
                'Код подтверждения неверен или пользователь отсутствует.')
        user_conf.delete()
        return data


class UsersViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password', 'role', 'email',
                  'bio', 'first_name', 'last_name', 'is_superuser')
        model = User
