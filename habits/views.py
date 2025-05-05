from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import CustomPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner, ReadOnly
from users.tasks import send_telegram_notification


class HabitCreateAPIView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitRetrieveAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )


class HabitListAPIView(ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, ReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitPersonalListAPIView(ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, ReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(owner=user)


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        habit = serializer.save()
        send_telegram_notification.delay(habit.owner.id)


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]
