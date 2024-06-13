from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
from django.db.models import Q


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(username=username) | Q(email=username) | Q(phone=username))
        except CustomUser.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
