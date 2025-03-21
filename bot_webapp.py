import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo
from dotenv import load_dotenv

# Логируем
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
ROCKET_URL = os.getenv("ROCKET_URL")

if not BOT_TOKEN:
    logger.error("❌ Токен не найден!")
    exit(1)

if not WEBAPP_URL:
    logger.warning("⚠️ WEBAPP_URL не установлен!")
if not ROCKET_URL:
    logger.warning("⚠️ ROCKET_URL не установлен!")

logger.info(f"✅ TELEGRAM_TOKEN: {BOT_TOKEN[:10]}********")
logger.info(f"✅ WEBAPP_URL: {WEBAPP_URL}")
logger.info(f"✅ ROCKET_URL: {ROCKET_URL}")

# Создаем бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher() # Инициализируем Dispatcher

# Функция /start
async def start_command(message: types.Message):
    logger.info(f" /start от {message.from_user.id}")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_btn = types.KeyboardButton(" Играть в Clicker", web_app=WebAppInfo(url=WEBAPP_URL))
    rocket_btn = types.KeyboardButton(" Играть в ракету", web_app=WebAppInfo(url=ROCKET_URL))
    keyboard.add(webapp_btn, rocket_btn)
    await message.answer("Привет! Выбери игру:", reply_markup=keyboard)

# Регистрируем обработчик
dp.message.register(start_command, commands=["start"])

# Функция запуска
async def main():
    try:
        logger.info("✅ Бот запущен...")
        await dp.start_polling(bot, skip_updates=True) # Используем dp.start_polling()
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())