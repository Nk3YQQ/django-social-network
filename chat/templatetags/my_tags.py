from django import template

from users.templatetags.users_tags import check_user_status

register = template.Library()


@register.filter()
def check_user_in_chat(obj, user):
    return obj.user_2 if obj.user_1 == user else obj.user_1


@register.filter()
def check_user_status_in_chat(obj, user):
    return obj.user_2.status if obj.user_1 == user else obj.user_1.status


@register.filter()
def check_users_status_in_chat(obj, user):
    user = check_user_in_chat(obj, user)

    return check_user_status(user.status)


@register.filter()
def check_user_status_in_chat(obj):
    return check_user_status(obj.status)


@register.simple_tag
def check_message_sender(obj, chat, user):
    if obj.sender == user:
        return 'You'

    return check_user_in_chat(chat, user)


@register.simple_tag
def check_div_position(sender, user):
    return 'right mb-4' if sender == user else 'left pb-4'


@register.simple_tag
def check_user_avatar_in_chat(obj, user):
    user = check_user_in_chat(obj, user)

    return f'/media/{user.avatar}' if user.avatar else '/media/users/profile/default-avatar.jpg'
