from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import UserConfirmation, User


class UserConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UserConfirmation


class UserJWTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password', 'role', 'email',
                  'bio', 'first_name', 'last_name')
        model = User

    def is_valid(self, raise_exception=False):
        email = self.context['request'].POST.get('email')
        UserOBJ = get_object_or_404(UserConfirmation, email=email)
        confirmation_code = self.context['request'].data['confirmation_code']
        if UserOBJ.confirmation_code != confirmation_code:
            raise ValidationError('Код подтверждения неверен')

        valid = super(UserJWTSerializer, self
                      ).is_valid(raise_exception=raise_exception)
        UserOBJ.delete()
        return valid


class UsersViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password', 'role', 'email',
                  'bio', 'first_name', 'last_name', 'is_superuser')
        model = User
