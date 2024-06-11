from django.urls import path

from chat.apps import ChatConfig
from chat.views import ChatDetailView, ChatListView, check_or_create_chat

app_name = ChatConfig.name

urlpatterns = [
    path("", ChatListView.as_view(), name="chat_list"),
    path("<int:pk>/", ChatDetailView.as_view(), name="chat_detail"),
    path("check/<int:pk>/", check_or_create_chat, name="check_or_create_chat"),
]
