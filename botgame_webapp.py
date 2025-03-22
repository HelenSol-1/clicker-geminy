import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
ROCKET_URL = os.getenv("ROCKET_URL")

if not BOT_TOKEN or not WEBAPP_URL or not ROCKET_URL:
    raise Exception("❌ Проверь .env: TELEGRAM_TOKEN, WEBAPP_URL и ROCKET_URL должны быть заданы")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def handle_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🚀 Играть в кликер", web_app=WebAppInfo(url=WEBAPP_URL)),
                KeyboardButton(text="👋 Старт")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Выбери действие:", reply_markup=keyboard)

# Обработчик нажатия "Старт"
@dp.message(lambda msg: msg.text == "👋 Старт")
async def handle_greeting(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✅ Да"),
                KeyboardButton(text="❌ Нет")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Привет! Я могу запустить для тебя игру. Хочешь начать?", reply_markup=keyboard)

# Обработчик ответа "Да"
@dp.message(lambda msg: msg.text == "✅ Да")
async def handle_yes(message: types.Message):
    await message.answer("Запускаем ракету 🚀")
    await message.answer(text="Открывай игру:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Ракета", web_app=WebAppInfo(url=ROCKET_URL))]],
        resize_keyboard=True
    ))

# Обработчик ответа "Нет"
@dp.message(lambda msg: msg.text == "❌ Нет")
async def handle_no(message: types.Message):
    await message.answer("Хорошо! Возвращайся, когда захочешь 😊")

# Запуск
async def main():
    logger.info("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
