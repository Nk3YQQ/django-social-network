from django.utils import timezone

from users.models import User


def filter_users_in_friendship_list(friendship_list, current_user):
    return list(
        friendship.user_2 if friendship.user_1 == current_user else friendship.user_1 for friendship in friendship_list
    )[:3]


def create_user():
    return User.objects.create(
        first_name="Test",
        last_name="Testov",
        email="test.testov@mail.ru",
        gender="Мужской",
        birthday_date=timezone.now(),
    )


def create_other_user():
    return User.objects.create(
        first_name="Ivan",
        last_name="Ivanov",
        email="ivan.ivanov@mail.ru",
        gender="Мужской",
        birthday_date=timezone.now(),
    )


def create_another_user():
    return User.objects.create(
        first_name="Petr",
        last_name="Petrov",
        email="petr.petrov@mail.ru",
        gender="Мужской",
        birthday_date=timezone.now(),
    )
