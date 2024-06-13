from django.db import models
from django.contrib.auth import get_user_model
from pytils.translit import slugify
from tinymce.models import HTMLField
from django.utils import timezone


User = get_user_model()


class City(models.Model):
    """
    Модель города
    """

    name = models.CharField(max_length=100, null=False, unique=True, verbose_name='Название')

    def __str__(self):
        return f'Город {self.name}'

    def short_str(self):
        return f'г. {self.name}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Street(models.Model):
    """
    Модель улицы
    """

    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, verbose_name='Город')
    name = models.CharField(max_length=150, null=False, verbose_name='Улица')

    def __str__(self):
        return f'{self.city.__str__()}, улица {self.name}'

    def short_str(self):
        return f'ул. {self.name}'

    def short_str_with_city(self):
        return f'{self.city.short_str()}, ул. {self.name}'

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'


class Address(models.Model):
    """
    Модель конечного адреса
    """

    street = models.ForeignKey(Street, on_delete=models.CASCADE, null=False, verbose_name='Улица')
    number = models.IntegerField(null=False, verbose_name='Номер здания')
    corpus = models.CharField(max_length=5, null=True, blank=True, verbose_name='Корпус')

    def __str__(self):
        corp = ''
        if self.corpus:
            corp = f', корпус {self.corpus}'
        return f'{self.street.__str__()}, дом {self.number}{corp}'

    def short_str(self):
        corp = ''
        if self.corpus:
            corp = f'/{self.corpus}'
        return f'{self.street.short_str()}, д. {self.number}{corp}'

    def short_str_with_city(self):
        corp = ''
        if self.corpus:
            corp = f'/{self.corpus}'
        return f'{self.street.short_str_with_city()}, д. {self.number}{corp}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Contract(models.Model):
    """
    Модель договора с клиентом
    """

    number = models.CharField(max_length=100, unique=True, verbose_name='Номер договора')
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name='Клиент',
                             related_name='user_contract')
    address = models.ForeignKey(Address, null=False, on_delete=models.CASCADE, verbose_name='Адрес клиента')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Договор с клиентом'
        verbose_name_plural = 'Договора с клиентами'


class RequestTheme(models.Model):
    """
    Модель темы заявки
    """
    name = models.CharField(max_length=150, null=False, verbose_name='Название темы')
    description = models.TextField(null=False, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тема заявки'
        verbose_name_plural = 'Темы заявки'


class Request(models.Model):
    """
    Модель заявки от клиента
    """

    STATUS_CHOICES = (
        (1, 'Новая'),
        (2, 'В работе'),
        (3, 'Закрыта'),
    )

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name='Клиент')
    theme = models.ForeignKey(RequestTheme, null=False, on_delete=models.CASCADE, verbose_name='Тема заявки')
    request = models.TextField(null=False, verbose_name='Текст заявки')
    status = models.IntegerField(choices=STATUS_CHOICES, null=False, verbose_name='Статус заявки')

    def __str__(self):
        return f"Заявка от {self.user.username}. Тема заявки: {self.theme.name}"

    class Meta:
        verbose_name = 'Заявка от клиента'
        verbose_name_plural = 'Заявки от клиентов'


class News(models.Model):
    """
    Модель новостей
    """

    STATUS_CHOICES = (
        (1, 'Черновик'),
        (2, 'Опубликована'),
    )

    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок новости")
    slug = models.SlugField(unique=True, max_length=200, null=False, blank=False, verbose_name="Слаг новости")
    content = HTMLField(null=False, blank=False, verbose_name="Контент новости")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    status = models.IntegerField(choices=STATUS_CHOICES, null=False, verbose_name='Статус новости')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self._state.adding:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        else:
            if slugify(self.title) != self.slug:
                base_slug = slugify(self.title)
                slug = base_slug
                num = 1
                while News.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{num}"
                    num += 1
                self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
