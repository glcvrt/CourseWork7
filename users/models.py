from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    VERSION_CHOICES = ((True, 'Действующий'), (False, 'Заблокирован'))

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='media/', verbose_name='фото', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    is_active = models.BooleanField(choices=VERSION_CHOICES, default=True, verbose_name='Статус пользователя')

    telegram_id = models.CharField(max_length=20, verbose_name='telegram_id', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
