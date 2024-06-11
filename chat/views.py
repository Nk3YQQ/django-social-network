from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from chat.forms import MessageForm
from chat.models import Chat, Message
from chat.services import filter_chat, filter_chat_by_model, filter_messages_by_date, filter_users_in_chat
from users.models import User


class ChatListView(LoginRequiredMixin, ListView):
    """Контроллер для вывода чатов у пользователя"""

    model = Chat

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_chat(queryset, self.request.user)


class ChatDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для вывода чата между двумя пользователями"""

    model = Chat
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        chat = self.object

        context_data["user"] = filter_users_in_chat(chat, self.request.user)
        context_data["grouped_messages"] = filter_messages_by_date(Message, chat)
        context_data["object_list"] = self.get_queryset()

        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_chat(queryset, self.request.user)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            chat = self.get_object()
            content = form.cleaned_data["content"]
            Message.objects.create(chat=chat, sender=request.user, content=content)
            return HttpResponseRedirect(request.path_info)
        return self.get(request, *args, **kwargs)


@login_required
def check_or_create_chat(request, pk):
    """Контроллер для проверки или создания чата"""

    current_user = request.user
    other_user = User.objects.get(pk=pk)

    chat = filter_chat_by_model(Chat, current_user, other_user)

    if not chat:
        chat = Chat.objects.create(user_1=current_user, user_2=other_user)

    return redirect(reverse("chat:chat_detail", kwargs={"pk": chat.pk}))
