from django.urls import path

from network.apps import NetworkConfig
from network.views import ChatListView, ChatDetailView, check_or_create_chat

app_name = NetworkConfig.name

urlpatterns = [
    path('chats/', ChatListView.as_view(), name='chat_list'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('chat/check/<int:pk>', check_or_create_chat, name='check_or_create_chat'),
]
