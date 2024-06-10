from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

NULLABLE = {"blank": True, "null": True}


class Gender(models.TextChoices):
    """Выбор пола"""

    MALE = "Мужской", "Мужской"
    FEMALE = "Женский", "Женский"


class User(AbstractUser):
    """Модель пользователя"""
    STATUS = [
        ("Онлайн", "Онлайн"),
        ("Оффлайн", "Оффлайн")
    ]

    username = None

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    gender = models.CharField(max_length=50, choices=Gender.choices, verbose_name="Пол")
    birthday_date = models.DateTimeField(verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to="users/profile/", verbose_name="Аватар", **NULLABLE)
    phone = models.IntegerField(verbose_name="Номер телефона", **NULLABLE)

    status = models.CharField(max_length=50, choices=STATUS, default='Оффлайн')
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
