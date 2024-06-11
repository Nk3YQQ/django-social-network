from django.contrib import admin

from friendship.models import Friendship


@admin.register(Friendship)
class Friendship(admin.ModelAdmin):
    list_display = ("user_1", "user_2", "status")
