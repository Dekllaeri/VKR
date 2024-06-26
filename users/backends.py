from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import CustomUser


class CustomUserBackend(ModelBackend):
    """
    Кастомный бекенд аутентификации для кастомной модели пользователя
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(username=username) | Q(email=username) | Q(phone=username))
        except CustomUser.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
