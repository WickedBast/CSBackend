from django.test import TestCase
from django.urls import reverse

from users.models import User
from members.models import Member
import requests


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.register_url = reverse('users:register')
        self.register_pw_url = reverse('users:registration password')
        return super().setUp()

    def tearDown(self) -> None:
        return super(BaseTest, self).tearDown()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        resp = self.client.post(self.register_url)
        self.assertEqual(resp.status_code, 200)  # 200

    def test_can_create_a_user(self):
        loc = requests.get(url="https://nominatim.openstreetmap.org/?",
                           params={
                               "street": "Dobra 56/66",
                               "format": "json",
                               "addressdetails": 1,
                               "extratags": 1,
                               "limit": 1,
                           }).json()

        data = {
            "email": "schnerb@gmail.com",
            "types": User.Types.INDIVIDUAL,
            "type": Member.Types.PROSPECT,
            "name": "Jean-Baptiste",
            "phone_number": "1011121314",
            "address": loc[0]["address"]["road"] + " " + loc[0]["address"]["house_number"],
            "city": loc[0]["address"]["city"],
            "zip_code": loc[0]["address"]["postcode"]
        }

        response = self.client.post(self.register_url, data=data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 201)


class RegisterPasswordTest(BaseTest):
    def test_can_view_page(self):
        response = self.client.post(self.register_pw_url)
        self.assertEqual(response.status_code, 200)

    def test_can_register_pw(self):
        data = {
            "password": "123456789A",
            "token": "abcToken"
        }
        response = self.client.post(self.register_pw_url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_can_t_register_a_bad_password_(self):
        data = {
            "password": "12",
            "token": "abcToken"
        }
        response = self.client.post(self.register_pw_url, data=data)
        self.assertEqual(response.status_code, 400)
