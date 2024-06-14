from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, Group
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Класс регистрации и настройки кастомной модели пользователя в административной панели
    """

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'surname', 'patronymic', 'email', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_admin', 'is_client')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'phone', 'is_superuser', 'is_admin', 'is_client')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    list_filter = ('is_superuser', 'is_admin', 'is_client', 'is_active')
