from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import (DurationValidator, ExclusiveHabitValidator,
                               PeriodicValidator, PleasantHabitValidator,
                               RelatedHabitValidator)


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedHabitValidator("related_habit"),
            DurationValidator("duration"),
            PleasantHabitValidator("is_pleasant", "related_habit", "reward"),
            PeriodicValidator("periodic"),
            ExclusiveHabitValidator("related_habit", "reward"),
        ]
