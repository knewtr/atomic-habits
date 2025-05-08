import json
from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.pro")
        self.habit = Habit.objects.create(
            name="шаги",
            owner=self.user,
            place="улица",
            time="19:00:00",
            action="пройти 2000 шагов",
            is_pleasant=False,
            periodic=2,
            reward="съесть сырок Б.Ю.Александров",
            duration=timedelta(days=2),
            related_habit=None,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.habit.name)

    def test_habit_create(self):
        url = reverse("habits:habit_create")
        data = {
            "name": "витамины",
            "place": "кухня",
            "time": "06:00",
            "action": "выпить 1 капсулу омега-3",
            "is_pleasant": False,
            "periodic": 5,
            "reward": "выпить чашку кофе",
            "is_public": True,
        }
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_delete(self):
        url = reverse("habits:habit_destroy", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        url = reverse("habits:habits_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "name": self.habit.name,
                    "owner": self.user.pk,
                    "place": self.habit.place,
                    "time": self.habit.time,
                    "action": self.habit.action,
                    "is_pleasant": self.habit.is_pleasant,
                    "related_habit": self.habit.related_habit,
                    "periodic": self.habit.periodic,
                    "reward": self.habit.reward,
                    "duration": "2 00:00:00",
                    "is_public": self.habit.is_public,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
