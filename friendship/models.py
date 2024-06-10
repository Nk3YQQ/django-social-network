from django.db import models


class FriendshipStatus(models.TextChoices):
    """Статус заявки в друзья"""

    PENDING = "pending", "Заявка отправлена"
    ACCEPTED = "accepted", "Друзья"
    REJECTED = "rejected", "Вы подписаны"


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
