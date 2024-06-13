from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import authenticate

from .models import CustomUser

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'password', 'name', 'surname', 'patronymic')


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'name', 'surname', 'patronymic')


class CustomTokenCreateSerializer(serializers.Serializer):
    identifier = serializers.CharField(label="Username or Email or Phone", write_only=True)
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False, write_only=True)
    auth_token = serializers.CharField(label="Auth Token", read_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        if identifier and password:
            user = authenticate(request=self.context.get('request'), username=identifier, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError('Must include "identifier" and "password".', code='authorization')

        attrs['user'] = user
        return attrs


class UserPatchSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ['email', 'phone']
