from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели CustomUser"""

    def create_user(self, username, email=None, phone=None, password=None, **extra_fields):
        if not username and not email and not phone:
            raise ValueError('The Email or Phone or Username must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, email=None, phone=None, password=password, **extra_fields)

    # def create_user(self, email=None, phone=None, username=None, password=None, **extra_fields):
    #     if not extra_fields.get('is_superuser') and not email and not phone:
    #         raise ValueError('Either email or phone must be provided')
    #     if not password:
    #         raise ValueError('Password must be provided')
    #
    #     email = self.normalize_email(email)
    #     if email and not username:
    #         username = email.split('@')[0]
    #     user = self.model(email=email, phone=phone, username=username, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user
    #
    # def create_superuser(self, username, password=None, **extra_fields):
    #     extra_fields.setdefault('is_superuser', True)
    #     extra_fields.setdefault('is_admin', True)
    #
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')
    #     if extra_fields.get('is_admin') is not True:
    #         raise ValueError('Superuser must have is_admin=True.')
    #
    #     return self.create_user(username=username, password=password, **extra_fields)
