from django.db.models import Q

from users.services import filter_users_in_friendship_list


class CheckerOnList:
    """Класс на проверку статуса дружбы между пользователями на странице поиска"""

    def __init__(self, friendship_model, current_user):
        self.friendship = friendship_model
        self.current_user = current_user

    def check_for_friendship(self, status):
        friendship_list = self.friendship.objects.filter(
            (Q(user_1=self.current_user) | Q(user_2=self.current_user)) & Q(status=status)
        )

        if status == "pending":
            return self.friendship.objects.filter(user_2=self.current_user, status="pending")

        return filter_users_in_friendship_list(friendship_list, self.current_user)

    def check_for_status_friendship(self, status, mode=None):
        if status == "accepted":
            return self.friendship.objects.filter(
                (Q(user_1=self.current_user) | Q(user_2=self.current_user)) & Q(status=status)
            ).exists()
        if mode == "receiver":
            return self.friendship.objects.filter(user_2=self.current_user, status=status).exists()
        return self.friendship.objects.filter(user_1=self.current_user, status=status).exists()


class CheckerOnPage:
    """Класс для проверки статуса дружбы между пользователями на странице пользователя"""

    def __init__(self, friendship_model, current_user, other_user):
        self.friendship = friendship_model
        self.current_user = current_user
        self.other_user = other_user

    def check_for_status_friendship(self, status):
        """ Проверка статуса дружбы между двумя пользователями """
        pass

    def is_potential_friend(self):
        """Проверка на потенциального друга"""
        return self.friendship.objects.filter(
            user_1=self.current_user, user_2=self.other_user, status="pending"
        ).exists()

    def is_friend(self):
        """Проверка на друга"""
        return self.friendship.objects.filter(
            Q(user_1=self.current_user, user_2=self.other_user)
            | Q(user_1=self.other_user, user_2=self.current_user) & Q(status="accepted")
        ).exists()

    def is_subscriber(self):
        """Проверка на подписчика"""
        friendship_list = self.friendship.objects.filter(
            Q(user_1=self.current_user, user_2=self.other_user)
            | Q(user_1=self.other_user, user_2=self.current_user) & Q(status="rejected")
        ).exists()

        return filter_users_in_friendship_list(friendship_list, self.current_user)

    def is_requested(self):
        """Проверка на пользователя, который отправил нам заявку в друзья"""
        friendship_list = self.friendship.objects.filter(
            user_1=self.current_user, user_2=self.other_user, status="pending"
        ).exists()

        return filter_users_in_friendship_list(friendship_list, self.current_user)

    def create_friendship_list(self):
        friendship_list = self.friendship.objects.filter(
            (Q(user_2=self.other_user) | Q(user_1=self.other_user)) & Q(status="accepted")
        )

        return filter_users_in_friendship_list(friendship_list, self.current_user)
