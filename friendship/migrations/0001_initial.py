# Generated by Django 4.2 on 2024-05-23 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Friendship",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Заявка отправлена"),
                            ("accepted", "Друзья"),
                            ("rejected", "Вы подписаны"),
                        ],
                        max_length=50,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "user_1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friendship_as_user_1",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь №1",
                    ),
                ),
                (
                    "user_2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friendship_as_user_2",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь №2",
                    ),
                ),
            ],
            options={
                "verbose_name": "дружба",
                "verbose_name_plural": "дружбы",
            },
        ),
    ]
