from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from friendship.models import Friendship
from friendship.services import FriendshipHandler
from users.models import User


class FriendshipActionView(View):
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

    def post(self, request, pk):
        action_function = self.get_action_function(pk)
        if action_function:
            action_function()
        return self._redirect()

    def _redirect(self):
        if self.view_kwargs is None:
            self.view_kwargs = {}
        return redirect(reverse(self.redirect_view_name, kwargs=self.view_kwargs))


class FriendshipActionListView(FriendshipActionView):
    """Базовый обработчик для действий дружбы в поиске друзей"""

    redirect_view_name = "users:user_list"


class FriendshipActionOnPageView(FriendshipActionView):
    """Базовый обработчик для действий дружбы на странице пользователя"""

    redirect_view_name = "users:user_detail"

    def post(self, request, pk):
        self.view_kwargs = {"pk": pk}
        return super().post(request, pk)


class CreateFriendshipListView(FriendshipActionListView):
    """Создание дружбы в поиске друзей"""

    action = "create"


class CancelApplicationListView(FriendshipActionListView):
    """Отмена дружбы в поиске друзей"""

    action = "cancel"


class AcceptApplicationListView(FriendshipActionListView):
    """Отправка запроса дружбы в поиске друзей"""

    action = "accept"


class RejectApplicationListView(FriendshipActionListView):
    """Отклонение запроса дружбы в поиске друзей"""

    action = "reject"


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
