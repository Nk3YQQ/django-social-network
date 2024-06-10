from django.utils import timezone

from users.models import User


class BaseUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.now = timezone.now()
        self.online_time = self.now - timezone.timedelta(minutes=5)


class UpdateUserLastActivityMiddleware(BaseUserMiddleware):
    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user = request.user
            user.last_activity = self.now

            if user.last_activity >= self.online_time:
                user.status = 'Онлайн'
            else:
                user.status = 'Оффлайн'

            user.save()

        return response


class CheckUserStatusMiddleware(BaseUserMiddleware):
    def __call__(self, request):
        response = self.get_response(request)

        User.objects.filter(last_activity__gte=self.online_time).update(status='Онлайн')
        User.objects.filter(last_activity__lt=self.online_time).update(status='Оффлайн')

        return response
