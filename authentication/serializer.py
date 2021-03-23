from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(default='default')

    class Meta:
        fields = '__all__'
        model = User
