from django.core.management import BaseCommand
from django.utils import timezone

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        superuser = User.objects.create(
            email='admin@mail.ru',
            first_name='Admin',
            last_name='Adminov',
            gender='male',
            birthday_date=timezone.now(),
            is_staff=True,
            is_superuser=True
        )

        superuser.set_password('908poi543tre')
        superuser.save()
