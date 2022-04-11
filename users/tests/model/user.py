from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.test import TestCase

from users.models import User


class UserModel(TestCase):
    def create_user(self, email, type, password):
        return User.objects.create_user(email=email, types=type, password=password)

    def create_superuser(self, email, type, password):
        return User.objects.create_superuser(email=email, types=type, password=password)

    def test_create_user_without_password(self):
        user = self.create_user(email="user@gmail.com", type="Individual", password="")

        self.assertTrue(isinstance(user, User))

        self.assertEqual(validate_email(user.email), None)
        self.assertEqual(user.types, User.Types.INDIVIDUAL)

        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_admin, False)

        user.set_password("user123456")

        self.assertEqual(validate_password(user.password), None)

    def test_create_superuser(self):
        superuser = self.create_superuser(email="superuser@gmail.com", type="Individual", password="")

        self.assertTrue(isinstance(superuser, User))

        self.assertEqual(validate_email(superuser.email), None)
        self.assertEqual(superuser.types, User.Types.INDIVIDUAL)
        self.assertEqual(validate_password(superuser.password), None)

        self.assertEqual(superuser.is_active, True)
        self.assertEqual(superuser.is_admin, True)
        self.assertEqual(superuser.is_superuser, True)

    def test_user_functions(self):
        user = self.create_user(email="user@gmail.com", type="Individual", password="")

        self.assertEqual(user.__str__(), user.email)
        self.assertEqual(user.has_perm("register"), user.is_admin)
        self.assertTrue(user.has_module_perms("CleanStock"))
