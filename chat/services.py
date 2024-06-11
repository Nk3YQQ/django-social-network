from itertools import groupby

from django.db.models import Q


def filter_users_in_chat(chat, current_user):
    return chat.user_2 if chat.user_1 == current_user else chat.user_1


def filter_chat(queryset, user):
    return queryset.filter(Q(user_1=user) | Q(user_2=user))


def filter_chat_by_model(model, current_user, other_user):
    return model.objects.filter(
        Q(user_1=current_user, user_2=other_user) | Q(user_1=other_user, user_2=current_user)
    ).first()


def filter_messages_by_date(message_model, chat):
    messages = message_model.objects.filter(chat=chat).order_by("created_at")

    return {date: list(items) for date, items in groupby(messages, key=lambda x: x.created_at.date())}


def create_chat(chat_model, user_1, user_2):
    return chat_model.objects.create(user_1=user_1, user_2=user_2)
