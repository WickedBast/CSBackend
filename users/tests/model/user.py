from django.test import TestCase
from users.models import User


class CreateUser(TestCase):
    def create_user(self, email, type, password):
        return User.objects.create_user(email=email, types=type, password=password)

    def test_create_user(self):
        user = self.create_user(email="example@gmail.com", type="Individual", password="")

        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.types, User.Types.INDIVIDUAL)
        self.assertEqual(user.is_active, False)
