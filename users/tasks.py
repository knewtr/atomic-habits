from celery import shared_task

from habits.models import Habit
from users.models import User
from users.services import send_telegram_message


@shared_task
def send_telegram_notification(user_id):
    """Отправляет уведомление в телеграм"""
    user = User.objects.get(id=user_id)
    habits = Habit.objects.filter(owner=user)
    for habit in habits:
        message = (
            f"Привет! Напоминаю, что в {habit.time} тебе необходимо {habit.action}"
        )
        send_telegram_message(user.tg_chat_id, message)
