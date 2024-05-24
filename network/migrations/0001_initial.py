# Generated by Django 4.2 on 2024-05-23 20:14

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
            name="Chat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "user_1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat_as_user_1",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь №1",
                    ),
                ),
                (
                    "user_2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat_as_user_2",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь №2",
                    ),
                ),
            ],
            options={
                "verbose_name": "чат",
                "verbose_name_plural": "чаты",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(verbose_name="Текст сообщения")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Время отправления")),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="network.chat", verbose_name="Чат"
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Отправитель",
                    ),
                ),
            ],
            options={
                "verbose_name": "сообщение",
                "verbose_name_plural": "сообщения",
            },
        ),
    ]
