from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели"""

    def create_user(self, username, email=None, phone=None, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем в базе данных
        """

        if not username and not email and not phone:
            raise ValueError('The Email or Phone or Username must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя
        """

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, email=None, phone=None, password=password, **extra_fields)
