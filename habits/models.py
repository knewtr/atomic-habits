from datetime import timedelta

from django.db import models

from config.settings import AUTH_USER_MODEL
from users.models import User


class Habit(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название привычки",
        help_text="Укажите название своей привычки",
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Владелец",
        on_delete=models.SET_NULL,
        related_name="habit",
        blank=True,
        null=True,
    )
    place = models.CharField(
        max_length=100,
        verbose_name="Место",
        help_text="Укажите место, где выполянется действие",
        blank=True,
        null=True,
    )
    time = models.TimeField(
        default="00:00",
        verbose_name="Время",
        help_text="Укажите время, когда выполняется действие",
        blank=True,
        null=True,
    )
    action = models.CharField(
        max_length=100,
        verbose_name="Действие",
        help_text="Укажите действие",
        blank=True,
        null=True,
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Укажите, если это приятная привычка",
        blank=True,
        null=True,
    )
    related_habit = models.ForeignKey(
        "Habit",
        on_delete=models.SET_NULL,
        related_name="habit",
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
        null=True,
    )
    periodic = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Укажите, сколько раз в неделю будет выполняться привычка",
        blank=True,
        null=True,
    )
    reward = models.CharField(
        max_length=250,
        verbose_name="Награда",
        help_text="Укажите награду за выполнение",
    )
    duration = models.DurationField(
        default=timedelta(seconds=120),
        verbose_name="Время выполнения",
        help_text="Укажите время выполнение",
        blank=True,
        null=True,
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        blank=True,
        null=True,
    )

    def __str___(self):
        return f"Я буду {self.action} в {self.time} в {self.place}."

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
