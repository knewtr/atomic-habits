import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.pro", name="test", avatar=None, tg_chat_id="test"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        url = reverse("users:user_detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_create(self):
        url = reverse("users:register")
        data = {
            "email": "test3@mail.pro",
            "password": "1234qwe",
            "name": "test2",
            "avatar": None,
            "tg_chat_id": "test2",
        }
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_delete(self):
        url = reverse("users:user_delete", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_user_list(self):
        url = reverse("users:user_list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.user.pk,
                "email": self.user.email,
                "name": self.user.name,
                "avatar": self.user.avatar,
                "tg_chat_id": self.user.tg_chat_id,
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
