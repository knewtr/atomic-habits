import json
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User
from users.tasks import send_telegram_notification


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


class NotificationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test5@mail.pro", name="test5", avatar=None, tg_chat_id="test5"
        )
        self.habit = Habit.objects.create(
            name="шаги",
            owner=self.user,
            place="улица",
            time="19:00:00",
            action="пройти 2000 шагов",
            is_pleasant=False,
            periodic=2,
            reward="съесть сырок Б.Ю.Александров",
            duration="00:02:00",
            related_habit=None,
            is_public=True,
        )

    @patch("users.services.send_telegram_message")
    def test_user_notification(self, mock_send):
        send_telegram_notification(self.user.id)
        self.assertEqual(mock_send.call_count, 1)

        expected_call = [
            (
                self.user.tg_chat_id,
                "Привет! Напоминаю, что в 19:00:00 тебе необходимо пройти 2000 шагов",
            ),
        ]
        actual_call = mock_send.call_args[0]
        self.assertEqual(actual_call, expected_call)
