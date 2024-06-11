from django.test import TestCase as BaseTestCase

from users.services import create_user, create_other_user


class TestCase(BaseTestCase):
    """ Базовый класс для тестирования модели """

    model = None

    def setUp(self):
        self.user_1 = create_user()
        self.user_2 = create_other_user()

    def object_create(self, object_data: dict):
        """Создание объекта"""

        return self.model.objects.create(**object_data)

    def get_object(self, pk):
        """Получение объекта"""

        return self.model.objects.get(pk=pk)

    def get_object_count(self):
        """Получение количества объектов"""

        return self.model.objects.count()

    def check_assertion_error(self, instance):
        with self.assertRaises(self.model.DoesNotExist):
            self.get_object(instance.pk)
