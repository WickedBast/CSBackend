from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.test import TestCase

from users.models import User


class BaseTestUser(TestCase):
    def setUp(self) -> None:
        self.email = "user@gmail.com"
        self.types = "Individual"
        self.password = ""

        self.user = User.objects.create_user(email=self.email,
                                             types=self.types,
                                             password=self.password)

        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()


class BaseTestSuperUser(TestCase):
    def setUp(self) -> None:
        self.email = "superuser@gmail.com"
        self.types = "Individual"
        self.password = "admin123456"

        self.superuser = User.objects.create_superuser(email=self.email,
                                                       types=self.types,
                                                       password=self.password)

        self.superuser.save()

    def tearDown(self) -> None:
        self.superuser.delete()


class UserModel(BaseTestUser):
    def test_create_user(self):
        self.assertTrue(isinstance(self.user, User))

        self.assertEqual(validate_email(self.user.email), None)
        self.assertEqual(self.user.types, User.Types.INDIVIDUAL)

        self.assertEqual(self.user.is_active, False)
        self.assertEqual(self.user.is_admin, False)

        self.user.set_password("user123456")

        self.assertEqual(validate_password(self.user.password), None)

    def test_user_functions(self):
        self.assertEqual(self.user.__str__(), self.user.email)
        self.assertEqual(self.user.__str__(), "user@gmail.com")
        self.assertEqual(self.user.has_perm("register"), self.user.is_admin)
        self.assertTrue(self.user.has_module_perms("CleanStock"))


class SuperUserModel(BaseTestSuperUser):
    def test_create_superuser(self):
        self.assertTrue(isinstance(self.superuser, User))

        self.assertEqual(validate_email(self.superuser.email), None)
        self.assertEqual(self.superuser.types, User.Types.INDIVIDUAL)
        self.assertEqual(validate_password(self.superuser.password, user=self.superuser), None)

        self.assertEqual(self.superuser.is_active, True)
        self.assertEqual(self.superuser.is_admin, True)
        self.assertEqual(self.superuser.is_superuser, True)

    def test_superuser_functions(self):
        self.assertEqual(self.superuser.__str__(), self.superuser.email)
        self.assertEqual(self.superuser.__str__(), "superuser@gmail.com")
        self.assertEqual(self.superuser.has_perm("register"), self.superuser.is_admin)
        self.assertTrue(self.superuser.has_module_perms("CleanStock"))
