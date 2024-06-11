from chat.models import Chat, Message
from chat.services import create_chat
from network.tests import TestCase


class MessageTestCase(TestCase):
    """Тестирование модели сообщения"""

    model = Message

    def setUp(self):
        super().setUp()

        self.chat = create_chat(Chat, self.user_1, self.user_2)

        self.message_data = {"chat": self.chat, "sender": self.user_1, "content": "Hi, Test!"}

    def create_message(self):
        """Создание сообщения"""

        return self.object_create(self.message_data)

    def test_message_create(self):
        """Тестирование создания сообщения"""

        message = self.create_message()

        self.assertTrue(self.get_object(pk=message.pk), True)

    def test_message_list(self):
        """Тестирование списка сообщений"""

        for _ in range(5):
            self.object_create(self.message_data)

        self.assertEqual(self.get_object_count(), 5)

    def test_message_update(self):
        """Тестирование обновления сообщения"""

        message = self.create_message()

        message.content = "Hi, Petr!"
        message.save()

        self.assertEqual(self.get_object(message.pk).content, "Hi, Petr!")

    def test_message_delete(self):
        """Тестирование удаления сообщения"""

        message = self.create_message()

        self.assertTrue(self.get_object(message.pk), True)

        message.delete()

        self.check_assertion_error(message)
