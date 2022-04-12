from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):

    def setUp(self) -> None:
        self.register_url = reverse('users:register')
        return super().setUp()

    def tearDown(self) -> None:
        return super(BaseTest, self).tearDown()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        resp = self.client.post(self.register_url)
        self.assertEqual(resp.status_code, 200)
