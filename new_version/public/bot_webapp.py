import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
GAME_URL = os.getenv("GAME_URL")

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота с правильной конфигурацией
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher() # Исправлено: Dispatcher создается без бота

@dp.message(commands=['start']) # Исправлено: message_handler заменен на message
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = types.KeyboardButton(" Играть", web_app=WebAppInfo(url=GAME_URL))
    keyboard.add(webapp_button)
    
    await message.answer("Привет! Нажми на кнопку ниже, чтобы сыграть в игру ", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot, skip_updates=True) # Бот передается при запуске

if __name__ == "__main__":
    asyncio.run(main())