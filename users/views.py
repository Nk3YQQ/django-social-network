from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from network.models import Friendship, FriendshipStatus
from users.forms import UserRegisterView
from users.models import User


class RegisterView(CreateView):
    """Контроллер для создания пользователя"""

    model = User
    form_class = UserRegisterView
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["intent"] = {"title": "Регистрация", "button": "Зарегистрироваться"}
        return context_data


class UserListView(ListView):
    """Контроллер для просмотра пользователей"""

    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(pk=self.request.user.pk).exclude(is_superuser=True).exclude()
        return queryset


class UserFriendshipListView(ListView):
    """ Контроллер для просмотра друзей """

    model = User
    template_name = 'users/user_friendship_list.html'

    def get_queryset(self):
        friendships = Friendship.objects.filter(
            (Q(user_1=self.request.user) | Q(user_2=self.request.user)) & Q(status=FriendshipStatus.ACCEPTED)
        )

        friends = []
        for friendship in friendships:
            if friendship.user_1 == self.request.user:
                friends.append(friendship.user_2)
            else:
                friends.append(friendship.user_2)

        return friends

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['friend_requests'] = Friendship.objects.filter(user_2=self.request.user, status='pending')
        return context_data


class UserDetailView(DetailView):
    """Контроллер для просмотра пользователя"""

    model = User

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['user_data'] = [
            {'name': 'Полное имя', 'value': self.object},
            {'name': 'Электронная почта', 'value': self.object.email},
            {'name': 'Пол', 'value': self.object.gender},
            {'name': 'Телефон', 'value': self.object.phone},
        ]
        friend = get_object_or_404(User, pk=self.kwargs['pk'])
        context_data['is_potential_friend'] = Friendship.objects.filter(user_1=self.request.user, user_2=friend,
                                                                        status='pending').exists()
        context_data['is_friend'] = Friendship.objects.filter(user_1=self.request.user, user_2=friend,
                                                              status='accepted').exists()
        return context_data


class UserUpdateView(UpdateView):
    """Контроллер для обновления пользователя"""

    model = User
    form_class = UserRegisterView

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.kwargs.get("pk")])


class UserDeleteView(DeleteView):
    """Контроллер для удаления пользователя"""

    model = User
    success_url = reverse_lazy("users:login")


class LoginView(BaseLoginView):
    """ Контроллер для входа в аккаунт """

    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["intent"] = {"title": "Вход", "button": "Войти"}
        return context_data


class LogoutView(BaseLogoutView):
    """ Контроллер для выхода из аккаунта """

    pass


def create_friendship_between_users(request, pk):
    current_user = request.user
    other_user = User.objects.get(pk=pk)

    friendship = (
            Friendship.objects.filter(Q(user_1=current_user, user_2=other_user)) |
            Friendship.objects.filter(Q(user_1=other_user, user_2=current_user))
    )

    if not friendship:
        friendship = Friendship.objects.create(user_1=current_user, user_2=other_user)
        friendship.status = 'pending'
        friendship.save()

    return redirect(reverse('users:user_detail', kwargs={'pk': pk}))


def cancel_application(request, pk):
    current_user = request.user
    other_user = User.objects.get(pk=pk)

    friendship = (
            Friendship.objects.filter(Q(user_1=current_user, user_2=other_user)) |
            Friendship.objects.filter(Q(user_1=other_user, user_2=current_user))
    )

    if friendship:
        friendship.delete()

    return redirect(reverse('users:user_detail', kwargs={'pk': pk}))


def menu_view(request):
    friend_requests_count = Friendship.objects.filter(user_2=request.user, status='pending').count()
    print(friend_requests_count)
    return render(request, 'includes/inc_network_menu.html', {'friend_requests_count': friend_requests_count})


def has_been_friend(request):
    friendship = Friendship.objects.filter(
        (Q(user_1=request.user) | Q(user_2=request.user)) & Q(status=FriendshipStatus.PENDING)
    ).first()

    if friendship:
        friendship.status = 'accepted'
        friendship.save()

    return redirect(reverse('users:user_friendship_list'))
