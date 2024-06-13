from rest_framework import serializers

from api_v1.models import *


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'content', 'updated_at']


class NewsCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['status'] = 1
        return super().create(validated_data)

    class Meta:
        model = News
        fields = ['title', 'content']


class NewsPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ['title', 'content', 'status']


class RequestSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 1
        return super().create(validated_data)

    class Meta:
        model = Request
        fields = ['id', 'theme', 'request']


class RequestListSerializer(serializers.ModelSerializer):

    author_fio = serializers.SerializerMethodField(method_name='get_author_fio')
    author_email = serializers.SerializerMethodField(method_name='get_author_email')
    author_phone = serializers.SerializerMethodField(method_name='get_author_phone')
    author_contract_number = serializers.SerializerMethodField(method_name='get_author_contract_number')
    author_contract_address = serializers.SerializerMethodField(method_name='get_author_contract_address')
    theme_name = serializers.SerializerMethodField(method_name='get_theme_name')
    status_name = serializers.SerializerMethodField(method_name='get_status_name')

    def get_author_fio(self, obj):
        if obj.user.patronymic:
            return f"{obj.user.surname} {obj.user.name} {obj.user.patronymic}"
        else:
            return f"{obj.user.surname} {obj.user.name}"

    def get_author_email(self, obj):
        return f"{obj.user.email}"

    def get_author_phone(self, obj):
        return f"{obj.user.phone}"

    def get_author_contract_number(self, obj):
        contract = obj.user.user_contract.first()
        return contract.number if contract else None

    def get_author_contract_address(self, obj):
        contract = obj.user.user_contract.first()
        return str(contract.address) if contract else None

    def get_theme_name(self, obj):
        return obj.theme.name

    def get_status_name(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Request
        fields = ['id', 'author_fio', 'author_email', 'author_phone',
                  'author_contract_number', 'author_contract_address',
                  'theme', 'theme_name', 'request', 'status', 'status_name']


class RequestPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ['id', 'status']
