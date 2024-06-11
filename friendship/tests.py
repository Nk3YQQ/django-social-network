from friendship.models import Friendship
from network.tests import TestCase


class FriendshipTestCase(TestCase):
    """Тестирование модели дружбы"""

    model = Friendship

    def setUp(self):
        super().setUp()

        self.friendship_data = {"user_1": self.user_1, "user_2": self.user_2, "status": "pending"}

    def create_friendship(self):
        """Создание дружбы"""

        return self.object_create(self.friendship_data)

    def test_friendship_create(self):
        """Тестирование создания дружбы"""

        friendship = self.create_friendship()

        self.assertTrue(self.get_object(friendship.pk), True)

    def test_friendship_list(self):
        """Тестирование списка дружб"""

        for _ in range(5):
            self.object_create(self.friendship_data)

        self.assertEqual(self.get_object_count(), 5)

    def test_friendship_update(self):
        """Тестирование обновления дружбы"""

        friendship = self.create_friendship()

        friendship.status = "accepted"
        friendship.save()

        friendship_status = self.get_object(friendship.pk).status

        self.assertEqual(friendship_status, "accepted")

    def test_friendship_delete(self):
        """Тестирование удаления дружбы"""

        friendship = self.create_friendship()

        self.assertTrue(self.get_object(friendship.pk), True)

        friendship.delete()

        self.check_assertion_error(friendship)
