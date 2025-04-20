from rest_framework.serializers import ValidationError


class ExclusiveHabitValidator:
    def __init__(self, related_habit, reward):
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, value):
        related_habit_ = value.get(self.related_habit)
        reward_ = value.get(self.reward)

        if related_habit_ and reward_:
            raise ValidationError(
                "У привычки не может одновременно быть и поле вознаграждения, и поле связанной привычки."
            )


class RelatedHabitValidator:
    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, value):
        related_habit_ = value.get(self.related_habit)

        if related_habit_:
            if not related_habit_.is_pleasant:
                raise ValidationError("Связанная привычка должна быть приятной.")


class DurationValidator:
    def __init__(self, duration):
        self.duration = duration

    def __call__(self, value):
        duration_ = value.get(self.duration)
        if duration_ and duration_.total_seconds() > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")


class PleasantHabitValidator:
    def __init__(self, is_pleasant, related_habit, reward):
        self.is_pleasant = is_pleasant
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, value):
        is_pleasant_ = value.get(self.is_pleasant)
        related_habit_ = value.get(self.related_habit)
        reward_ = value.get(self.reward)

        if is_pleasant_:
            if related_habit_ or reward_:
                raise ValidationError(
                    "У приятной привычки не может быть награды или связанной привычки."
                )


class PeriodicValidator:
    def __init__(self, periodic):
        self.periodic = periodic

    def __call__(self, value):
        periodic_ = value.get(self.periodic)
        if periodic_ is not None and not 1 < periodic_ <= 7:
            raise ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в неделю, или чаще 7 раз в неделю."
            )
