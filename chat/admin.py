from django.contrib import admin

from chat.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("user_1", "user_2")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "chat", "sender")
