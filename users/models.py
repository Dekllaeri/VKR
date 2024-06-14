from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Модель кастомного пользователя
    """

    username = models.CharField(verbose_name="Никнейм", max_length=150, unique=True)
    name = models.CharField(verbose_name="Имя", max_length=150, blank=True)
    surname = models.CharField(verbose_name="Фамилия", max_length=150, blank=True)
    patronymic = models.CharField(verbose_name="Отчество", max_length=150, blank=True)
    email = models.EmailField(verbose_name="Электронная почта", unique=True, null=True, blank=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=15, unique=True, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    is_superuser = models.BooleanField(verbose_name="Является суперпользователем", default=False)
    is_admin = models.BooleanField(verbose_name="Является администратором", default=False)
    is_client = models.BooleanField(verbose_name="Является клиентом", default=False)

    date_joined = models.DateTimeField(verbose_name="Дата присоединения", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        u = ""
        p = ""
        if self.username:
            u = f"{self.username} / "
        if self.phone:
            u = f" / {self.phone}"

        return f"{u}{self.surname} {self.name}{p}"

    def save(self, *args, **kwargs):
        if self.email and not self.username:
            self.username = self.email.split('@')[0]
        if self.is_superuser or self.is_admin:
            self.email = None
            self.phone = None
        super(CustomUser, self).save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_superuser or self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
