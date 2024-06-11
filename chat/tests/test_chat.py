from chat.models import Chat
from network.tests import TestCase
from users.services import create_another_user


class ChatTestCase(TestCase):
    """Тестирование модели чата"""

    model = Chat

    def setUp(self):
        super().setUp()

        self.user_3 = create_another_user()

        self.object_data = {"user_1": self.user_1, "user_2": self.user_2}

    def create_chat(self):
        """Создание чата"""

        return self.object_create(self.object_data)

    def test_chat_create(self):
        """Тестирование создания чата"""

        chat = self.create_chat()

        self.assertTrue(self.get_object(chat.pk), True)

    def test_chat_list(self):
        """Тестирование списка чатов"""

        for _ in range(5):
            self.object_create(self.object_data)

        self.assertEqual(self.get_object_count(), 5)

    def test_chat_update(self):
        """Тестирование обновления чата"""

        chat = self.create_chat()

        chat.user_1 = self.user_3
        chat.save()

        user_1_email = self.get_object(chat.pk).user_1.email

        self.assertEqual(user_1_email, "petr.petrov@mail.ru")

    def test_chat_delete(self):
        """Тестирование удаления чата"""

        chat = self.create_chat()

        self.assertTrue(self.get_object(chat.pk), True)

        chat.delete()

        self.check_assertion_error(chat)
