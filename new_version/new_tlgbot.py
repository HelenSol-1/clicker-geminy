import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)  # Устанавливаем DEBUG-уровень логов
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
GAME_URL = os.getenv("GAME_URL")

if not BOT_TOKEN:
    logger.error("❌ Ошибка: TELEGRAM_TOKEN не найден!")
    exit(1)

if not GAME_URL:
    logger.warning("⚠️ Внимание: Переменная GAME_URL не задана.")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(commands=['start'])
async def start_command(message: types.Message):
    logger.info(f"📩 Получена команда /start от {message.from_user.id}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = types.KeyboardButton("🚀 Играть", web_app=WebAppInfo(url=GAME_URL))
    keyboard.add(webapp_button)

    await message.answer("Привет! Нажми на кнопку ниже, чтобы сыграть в игру 🚀", reply_markup=keyboard)

async def main():
    logger.info("✅ Бот запущен и ожидает команды...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
