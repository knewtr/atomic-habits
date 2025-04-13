import requests

from config import settings


def send_telegram_message(chat_id, message):
    params = {
        'text': message,
        'chat_id': chat_id,
    }
    requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)

# if __name__ == "__main__":
#     send_message('Привет', 123456)  # пользователю 123456 ушло сообщение "Привет"