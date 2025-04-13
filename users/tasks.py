from celery import shared_task
from users.services import send_telegram_message

from habits.models import Habit

@shared_task
def send_telegram_notification(owner):
    """Отправляет уведомление в телеграм"""
    user = User.objects.get(id=user_id)
    habit = Habit.objects.filter(owner=user)
    for habit in habits:
        message = f"Привет! Напоминаю, что в {habit.time} тебе необходимо {habit.action}"
        send_telegram_message(user.tg_chat_id, message)