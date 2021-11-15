import telegram
from backend.schemas.configuration import ConfigTelegram


# get chat id of user by chatting with https://t.me/jsondumpbot
def send_test_message(bot: ConfigTelegram, chat_id: int, message: str):
    try:
        telegram_notify = telegram.Bot(bot.token)
        telegram_notify.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
    except Exception as ex:
        print(ex)
        return str(ex)
