from django import template

register = template.Library()


@register.filter()
def check_request_user(obj):
    pass
