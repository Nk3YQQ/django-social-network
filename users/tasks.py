from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_users_status():
    now = timezone.now()
    online_time = now - timedelta(minutes=5)
    User.objects.filter(last_activity__gte=online_time).update(status='Онлайн')
    User.objects.filter(last_activity__lt=online_time).update(status='Оффлайн')
