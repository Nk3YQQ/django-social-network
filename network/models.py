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


class FriendshipStatus(models.TextChoices):
    """Статус заявки в друзья"""

    PENDING = "pending", "Заявка отправлена"
    ACCEPTED = "accepted", "Друзья"
    REJECTED = "rejected" "Вы подписаны"


class Friendship(models.Model):
    """Модель для дружбы"""

    user_1 = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь №1", related_name="friendship_as_user_1"
    )
    user_2 = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь №2", related_name="friendship_as_user_2"
    )

    status = models.CharField(max_length=50, choices=FriendshipStatus.choices, verbose_name="Статус")

    def __str__(self):
        return f"Friendship between {self.user_1} in {self.user_2} with status {self.status}"

    class Meta:
        verbose_name = "дружба"
        verbose_name_plural = "дружбы"
