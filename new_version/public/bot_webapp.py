import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext

# 🔹 Загружаем переменные из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GAME_URL = os.getenv("GAME_URL")

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("🚀 Играть", web_app=WebAppInfo(url=GAME_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Нажми кнопку, чтобы запустить игру!", reply_markup=reply_markup)

# 🔹 Создаем бота и добавляем команду /start
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# 🔹 Запускаем бота
print("✅ Бот запущен. Нажми /start в Telegram!")
app.run_polling()
