from django.utils import timezone

from network.tests import TestCase
from users.models import User


class UserTestCase(TestCase):
    """Тестирование модели пользователя"""

    model = User

    def setUp(self):
        super().setUp()

        self.user_1.delete()
        self.user_2.delete()

        self.user_data = {
            "first_name": "Test",
            "last_name": "Testov",
            "email": "test.testov@mail.ru",
            "gender": "Мужской",
            "birthday_date": timezone.now(),
        }

    def create_user(self):
        """Создание пользователя"""

        return self.object_create(self.user_data)

    def test_user_create(self):
        """Тестирование создания пользователя"""

        user = self.create_user()

        self.assertTrue(self.get_object(user.pk), True)

    def test_user_list(self):
        """Тестирование списка пользователей"""
        count = 0

        for _ in range(5):
            self.object_create(self.user_data)

            count += 1

            first_name = self.user_data.get("first_name").lower()
            last_name = self.user_data.get("last_name").lower()

            first_name += f"{count}"

            self.user_data["email"] = f"{first_name}{last_name}@mail.ru"

        self.assertEqual(self.get_object_count(), 5)

    def test_user_update(self):
        """Тестирование обновления пользователя"""

        user = self.create_user()

        user.first_name = "Petr"
        user.status = "Онлайн"
        user.save()

        user_name = self.get_object(user.pk).first_name
        user_status = self.get_object(user.pk).status

        self.assertEqual(user_name, "Petr")
        self.assertEqual(user_status, "Онлайн")

    def test_user_delete(self):
        """Тестирование обновления пользователя"""

        user = self.create_user()

        self.assertTrue(self.get_object(user.pk), True)

        user.delete()

        self.check_assertion_error(user)
