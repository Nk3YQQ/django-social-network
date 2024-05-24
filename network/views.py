from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from network.forms import MessageForm
from network.models import Chat, Message
from users.models import User


class ChatListView(ListView):
    """Контроллер для вывода чатов у пользователя"""

    model = Chat

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(user_1=self.request.user)) | queryset.filter(Q(user_2=self.request.user))
        return queryset


class ChatDetailView(DetailView):
    """Контроллер для вывода чата между двумя пользователями"""

    model = Chat
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["form"] = self.form_class()
        if self.request.user == self.object.user_1:
            context_data["object_list"] = Chat.objects.filter(user_1=self.request.user)
            context_data["user_pk"] = self.object.user_2.pk
        else:
            context_data["object_list"] = Chat.objects.filter(user_2=self.request.user)
            context_data["user_pk"] = self.object.user_1.pk

        context_data["messages"] = Message.objects.filter(chat=self.object)

        return context_data

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            chat = self.get_object()
            content = form.cleaned_data["content"]
            Message.objects.create(chat=chat, sender=request.user, content=content)
            return HttpResponseRedirect(request.path_info)
        return self.get(request, *args, **kwargs)


def check_or_create_chat(request, pk):
    """ Контроллер для проверки или создания чата"""

    current_user = request.user
    other_user = User.objects.get(pk=pk)

    chat = (
            Chat.objects.filter(Q(user_1=current_user, user_2=other_user))
            | Chat.objects.filter(Q(user_1=other_user, user_2=current_user))
    ).first()

    if not chat:
        chat = Chat.objects.create(user_1=current_user, user_2=other_user)

    return redirect(reverse("network:chat_detail", kwargs={"pk": chat.pk}))
