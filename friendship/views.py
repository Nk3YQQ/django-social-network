from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from friendship.models import Friendship
from friendship.services import FriendshipHandler
from users.models import User


class FriendshipActionView(LoginRequiredMixin, View):
    """Базовый обработчик для модели дружбы"""

    action = None
    view_kwargs = None
    redirect_view_name = None

    model = Friendship
    user_model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = None

    def dispatch(self, request, *args, **kwargs):
        self.current_user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_action_function(self, pk):
        handler = FriendshipHandler(self.model, self.current_user, self.user_model, pk)

        action_map = {
            "create": handler.create_friendship,
            "cancel": handler.cancel_friendship,
            "accept": handler.accept_friendship,
            "reject": handler.reject_friendship,
        }
        return action_map.get(self.action)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        action_function = self.get_action_function(pk)
        if action_function:
            action_function()
        return self._redirect()

    def _redirect(self):
        if self.view_kwargs is None:
            self.view_kwargs = {}
        return redirect(reverse(self.redirect_view_name, kwargs=self.view_kwargs))


class FriendshipActionOnPageView(FriendshipActionView):
    """Базовый обработчик для действий дружбы на странице пользователя"""

    redirect_view_name = "users:user_detail"

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.view_kwargs = {"pk": pk}
        return super().post(request, pk)


class CreateFriendshipListView(FriendshipActionView):
    """Создание дружбы в поиске друзей"""

    action = "create"
    redirect_view_name = "users:user_list"


class CancelApplicationListView(FriendshipActionView):
    """Отмена дружбы в поиске друзей"""

    action = "cancel"
    redirect_view_name = "users:user_requests_list"


class AcceptApplicationListView(FriendshipActionView):
    """Отправка запроса дружбы в поиске друзей"""

    action = "accept"
    redirect_view_name = "users:user_friendship_list"


class RejectApplicationListView(FriendshipActionView):
    """Отклонение запроса дружбы в поиске друзей"""

    action = "reject"
    redirect_view_name = "users:user_rejected_list"


class CreateFriendshipOnPageView(FriendshipActionOnPageView):
    """Создание дружбы на странице пользователя"""

    action = "create"


class CancelApplicationOnPageView(FriendshipActionOnPageView):
    """Отмена дружбы на странице пользователя"""

    action = "cancel"


class AcceptApplicationOnPageView(FriendshipActionOnPageView):
    """Отправка запроса дружбы на странице пользователя"""

    action = "accept"


class RejectApplicationOnPageView(FriendshipActionOnPageView):
    """Отклонение запроса дружбы на странице пользователя"""

    action = "reject"


def friend_request(request):
    """ Обработчик показывает, сколько друзей у пользователя """

    current_user = request.user

    if current_user.is_authenticated:
        friend_requests_count = Friendship.objects.filter(user_2=current_user, status="pending").count()

    else:
        friend_requests_count = 0

    return {'friend_requests_count': friend_requests_count}
