from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'patronymic', 'email', 'phone',
                  'username', 'is_superuser', 'is_admin', 'is_client']


class AuthSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')
        user = None

        if '@' in identifier:
            user = User.objects.filter(email=identifier).first()
        elif identifier.isdigit():
            user = User.objects.filter(phone=identifier).first()
        else:
            user = User.objects.filter(username=identifier).first()

        if user and user.check_password(password):
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Invalid credentials')
