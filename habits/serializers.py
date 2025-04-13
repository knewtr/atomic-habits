from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import RewardValidator, DurationValidator, PleasantHabitValidator, PeriodicValidator


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [RewardValidator("related_habit"), DurationValidator("duration"), PleasantHabitValidator("is_pleasant", "related_habit", "reward"), PeriodicValidator("periodic"),]
