from django.db.models import Q

from users.services import filter_users_in_friendship_list


class CheckerOnList:
    """Класс на проверку статуса дружбы между пользователями на странице поиска"""

    def __init__(self, friendship_model, user_model, current_user):
        self.friendship = friendship_model
        self.user_model = user_model
        self.current_user = current_user

    def check_for_friendship(self, status=None, receiving=False):
        if status:
            if status == "pending":
                if receiving:
                    friendship_list = self.friendship.objects.filter(user_2=self.current_user, status="pending")
                else:
                    friendship_list = self.friendship.objects.filter(user_1=self.current_user, status="pending")

            else:
                friendship_list = self.friendship.objects.filter(
                    (Q(user_1=self.current_user) | Q(user_2=self.current_user)) & Q(status=status)
                )

            return filter_users_in_friendship_list(friendship_list, self.current_user)
        else:
            friends = self.friendship.objects.filter(
                Q(user_1=self.current_user) | Q(user_2=self.current_user)
            ).values_list('user_1', 'user_2')

            friends_list = list(friend for sublist in friends for friend in sublist)

            return self.user_model.objects.exclude(
                Q(pk__in=friends_list) | Q(pk=self.current_user.pk)
            ).exclude(is_superuser=True)


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

        return self.friendship.objects.filter(
            Q(user_1=self.current_user, user_2=self.other_user)
            | Q(user_1=self.other_user, user_2=self.current_user) & Q(status="rejected")
        ).exists()

    def is_requested(self):
        """Проверка на пользователя, который отправил нам заявку в друзья"""

        return self.friendship.objects.filter(
            user_1=self.other_user, user_2=self.current_user, status="pending"
        ).exists()

    def create_friendship_list(self):
        friendship_list = self.friendship.objects.filter(
            (Q(user_2=self.other_user) | Q(user_1=self.other_user)) & Q(status="accepted")
        )

        return filter_users_in_friendship_list(friendship_list, self.other_user)
