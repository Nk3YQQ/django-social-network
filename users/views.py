from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from friendship.models import Friendship
from users.checkers import CheckerOnList, CheckerOnPage
from users.forms import UserRegisterView
from users.models import User


class RegisterView(CreateView):
    """Контроллер для создания пользователя"""

    model = User
    form_class = UserRegisterView
    template_name = "users/registration.html"

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["intent"] = {"title": "Регистрация", "button": "Зарегистрироваться"}
        return context_data


class UserListView(LoginRequiredMixin, ListView):
    """Базовый контроллер для просмотра всех пользователей"""

    model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checker = None

    def dispatch(self, request, *args, **kwargs):
        self.checker = CheckerOnList(Friendship, self.model, self.request.user)
        return super().dispatch(request, *args, **kwargs)


class UserAllListView(UserListView):
    """Контроллер для просмотра всех пользователей"""

    def get_queryset(self):
        return self.checker.check_for_friendship()


class UserFriendshipListView(UserListView):
    """Контроллер для просмотра друзей"""

    template_name = "users/user_friendship_list.html"

    def get_queryset(self):
        return self.checker.check_for_friendship(status="accepted")


class UserRequestsListView(UserListView):
    """Контроллер для просмотра отправленных заявок"""

    template_name = "users/user_requests_list.html"

    def get_queryset(self):
        return self.checker.check_for_friendship(status="pending")


class UserReceiversListView(UserListView):
    """Контроллер для просмотра заявок в друзья от других пользователей"""

    template_name = "users/user_receiver_list.html"

    def get_queryset(self):
        return self.checker.check_for_friendship(status="pending", receiving=True)


class UserRejectedListView(UserListView):
    """Контроллер для просмотра подписчиков"""

    template_name = "users/user_rejected_list.html"

    def get_queryset(self):
        return self.checker.check_for_friendship(status="rejected")


class UserDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра пользователя"""

    model = User

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        current_user = self.request.user

        other_user = get_object_or_404(User, pk=self.kwargs["pk"])

        checker = CheckerOnPage(Friendship, current_user, other_user)

        friend_list = checker.create_friendship_list()

        context_data["user_data"] = [
            {"name": "Полное имя", "value": self.object},
            {"name": "Электронная почта", "value": self.object.email},
            {"name": "Пол", "value": self.object.gender},
            {"name": "Телефон", "value": self.object.phone if self.object.phone else "Отсутствует"},
        ]
        context_data["other_user"] = other_user
        context_data["is_potential_friend"] = checker.is_potential_friend()
        context_data["is_friend"] = checker.is_friend()
        context_data["friend_list"] = friend_list
        context_data["is_subscriber"] = checker.is_subscriber()
        context_data["is_requested"] = checker.is_requested()
        context_data["friend_count"] = len(friend_list)

        return context_data


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для обновления пользователя"""

    model = User
    form_class = UserRegisterView

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.kwargs.get("pk")])


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления пользователя"""

    model = User
    success_url = reverse_lazy("users:login")


class LoginView(BaseLoginView):
    """Контроллер для входа в аккаунт"""

    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["intent"] = {"title": "Вход", "button": "Войти"}
        return context_data


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    """Контроллер для выхода из аккаунта"""

    pass


class RedirectToCurrentUserProfile(LoginRequiredMixin, View):
    """Контроллер для перехода на страницу текущего пользователя"""

    def get(self, request):
        current_user_pk = self.request.user.pk

        return redirect(reverse("users:user_detail", kwargs={"pk": current_user_pk}))
