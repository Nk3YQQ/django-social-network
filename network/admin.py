from django.contrib import admin

from network.models import Chat, Message, Friendship


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user_1', 'user_2')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'chat', 'sender')


@admin.register(Friendship)
class Friendship(admin.ModelAdmin):
    list_display = ('user_1', 'user_2', 'status')
