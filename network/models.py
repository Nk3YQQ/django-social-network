from django.db import models


class Chat(models.Model):
    """Модель для чата"""

    user_1 = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь №1", related_name="chat_as_user_1"
    )
    user_2 = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь №2", related_name="chat_as_user_2"
    )

    def __str__(self):
        return f"Chat №{self.pk}"

    class Meta:
        verbose_name = "чат"
        verbose_name_plural = "чаты"


class Message(models.Model):
    """Модель для сообщения"""

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name="Чат")
    sender = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Отправитель")

    content = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время отправления")

    def __str__(self):
        return f"Message from {self.sender} in {self.chat}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
