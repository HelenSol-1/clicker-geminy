import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo
from dotenv import load_dotenv

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
GAME_URL = os.getenv("GAME_URL")  # Основная игра
ROCKET_URL = os.getenv("ROCKET_GAME_URL")  # Игра с ракетой

if not BOT_TOKEN:
    logger.error("❌ Ошибка: TELEGRAM_TOKEN не найден!")
    exit(1)
if not GAME_URL:
    logger.warning("⚠️ Внимание: Переменная GAME_URL не задана.")
if not ROCKET_URL:
    logger.warning("⚠️ Внимание: Переменная ROCKET_GAME_URL не задана.")

logger.info(f"✅ TELEGRAM_TOKEN загружен: {BOT_TOKEN[:10]}********")
logger.info(f"✅ GAME_URL загружен: {GAME_URL}")
logger.info(f"✅ ROCKET_licker-geminy загружен: {ROCKET_URL}")

# Создаём бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(commands=['start'])
async def start_command(message: types.Message):
    logger.info(f"📩 Получена команда /start от {message.from_user.id}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = types.KeyboardButton("🎮 Играть в Clicker", web_app=WebAppInfo(url=GAME_URL))
    rocket_button = types.KeyboardButton("🚀 Играть в ракету", web_app=WebAppInfo(url=ROCKET_URL))
    keyboard.add(webapp_button, rocket_button)

    await message.answer("Привет! Выбери игру:", reply_markup=keyboard)

async def main():
    logger.info("✅ Бот запущен и ожидает команды...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
