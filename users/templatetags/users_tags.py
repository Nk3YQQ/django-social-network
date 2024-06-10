from django import template

register = template.Library()


@register.filter()
def check_user_status(obj):
    return '/media/users/status/online.jpg' if obj == 'Онлайн' else '/media/users/status/offline.png'


@register.filter()
def check_user_avatar(obj):
    return f'/media/{obj}' if obj else '/media/users/profile/default-avatar.jpg'
