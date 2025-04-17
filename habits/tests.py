import json

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
            time="19:00",
            action="пройти 2000 шагов",
            is_pleasant=False,
            periodic=2,
            reward="съесть сырок Б.Ю.Александров",
            is_public=True
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
            "is_pleasant": "False",
            "periodic": "5",
            "reward": "выпить чашку кофе",
            "is_public": "True",
        }
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    # def test_habit_update(self):
    #     url = reverse("habits:habit_update", args=(self.habit.pk,))
    #     data = {"reward": "выпить кружку вкусного чая"}
    #     response = self.client.patch(url, data)
    #     data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("reward"), "выпить кружку вкусного чая")

    def test_habit_delete(self):
        url = reverse("habits:habit_destroy", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

