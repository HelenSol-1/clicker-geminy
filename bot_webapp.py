import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
ROCKET_URL = os.getenv("ROCKET_URL")

# Логирование
logging.basicConfig(level=logging.INFO)

# Проверяем переменные
if not TOKEN:
    logging.error("❌ TELEGRAM_TOKEN не найден!")
    exit(1)
if not WEBAPP_URL:
    logging.warning("⚠️ WEBAPP_URL не задан.")
if not ROCKET_URL:
    logging.warning("⚠️ ROCKET_URL не задан.")

# Создаём бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = types.KeyboardButton("🎮 Играть в Clicker", web_app=WebAppInfo(url=WEBAPP_URL))
    rocket_button = types.KeyboardButton("🚀 Играть в Ракету", web_app=WebAppInfo(url=ROCKET_URL))
    keyboard.add(webapp_button, rocket_button)

    await message.answer("Выбери игру:", reply_markup=keyboard)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
