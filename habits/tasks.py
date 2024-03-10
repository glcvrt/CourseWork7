import requests
from celery import shared_task
from django.conf import settings

from config.settings import TELEGRAM_CHAT_ID, TELEGRAM_BOT_API_KEY
from habits.models import Habit

bot_token = TELEGRAM_BOT_API_KEY
telegram_id = TELEGRAM_CHAT_ID
get_id_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'


@shared_task
def send_message_to_bot(habit_id):
    """ функция отправки сообщения в телеграм-бот
    chat_id: id чата
    message: передаваемое сообщение
    """
    habit = Habit.objects.get(id=habit_id)
    requests.get(
        url=f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_API_KEY}/sendMessage',
        params={
            'chat_id': habit.user.telegram_id,
            'text': f'Привет {habit.user}! Время {habit.time}. Пора идти в {habit.place} и сделать {habit.action}. ' \
                    f'Это займет {habit.duration} минут!'
        }
    )
