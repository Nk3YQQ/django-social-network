from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Gender(models.TextChoices):
    MALE = 'male', 'Мужской'
    FEMALE = 'female', 'Женский'


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    gender = models.CharField(max_length=50, choices=Gender.choices, verbose_name='Пол')
    birthday_date = models.DateTimeField(verbose_name='Дата рождения')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.IntegerField(verbose_name='Номер телефона', **NULLABLE)
