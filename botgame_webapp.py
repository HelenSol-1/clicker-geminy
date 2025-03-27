import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
ROCKET_URL = os.getenv("ROCKET_URL")

if not BOT_TOKEN:
    logger.error("❌ TELEGRAM_TOKEN не найден!")
    exit(1)
if not WEBAPP_URL:
    logger.warning("⚠️ WEBAPP_URL не задан!")
if not ROCKET_URL:
    logger.warning("⚠️ ROCKET_URL не задан!")

logger.info(f"✅ TELEGRAM_TOKEN загружен: {BOT_TOKEN[:10]}********")
logger.info(f"✅ WEBAPP_URL загружен: {WEBAPP_URL}")
logger.info(f"✅ ROCKET_URL загружен: {ROCKET_URL}")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(F.text.lower() == "/start")
async def handle_start(message: types.Message):
    logger.info(f"📩 /start от {message.from_user.id}")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👋 Старт")],
            [KeyboardButton(text="🚀 Играть", web_app=WebAppInfo(url=ROCKET_URL))],
            [KeyboardButton(text="💬 Поговорим позже")]
        ],
        resize_keyboard=True
    )
    await message.answer("Привет! Я бот, который умеет запускать игры. Выбери действие:", reply_markup=keyboard)

@dp.message(F.text == "👋 Старт")
async def handle_hello(message: types.Message):
    await message.answer("Привет-привет! 😊")

@dp.message(F.text == "💬 Поговорим позже")
async def handle_later(message: types.Message):
    await message.answer(
        "Хорошо, поговорим позже. Возвращайся, когда будешь готов!",
        reply_markup=ReplyKeyboardRemove()
    )

async def main():
    logger.info("✅ Бот запущен")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
