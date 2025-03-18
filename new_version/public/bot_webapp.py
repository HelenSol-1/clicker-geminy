import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

# ✅ Загружаем переменные из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
GAME_URL = os.getenv("GAME_URL")

# ✅ Настраиваем логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ✅ Проверяем наличие переменных окружения
if not BOT_TOKEN:
    logger.error("❌ Ошибка: TELEGRAM_TOKEN не найден! Проверь .env!")
    exit(1)
if not GAME_URL:
    logger.warning("⚠️ Внимание: Переменная GAME_URL не задана.")

logger.info(f"✅ TELEGRAM_TOKEN загружен: {BOT_TOKEN[:10]}********")
logger.info(f"✅ GAME_URL загружен: {GAME_URL}")

# ✅ Создаем бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ✅ Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    logger.info(f"📩 Получена команда /start от {message.from_user.id}")

    # Создаем клавиатуру с кнопкой WebApp
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = types.KeyboardButton("🚀 Играть в ракету", web_app=WebAppInfo(url=GAME_URL))
    keyboard.add(webapp_button)

    # Отправляем сообщение пользователю
    result = await message.answer(f"Привет, {hbold(message.from_user.first_name)}!\n"
                                  "Нажми на кнопку ниже, чтобы сыграть в игру 🚀",
                                  reply_markup=keyboard)
    
    logger.info(f"✅ Сообщение отправлено? {bool(result)}")
    print(f"✅ Сообщение отправлено? {bool(result)}")  # Выводим в консоль для отладки

# ✅ Функция запуска бота
async def main():
    logger.info("✅ Бот запущен и ожидает команды...")
    print("✅ Бот запущен и ожидает команды...")  # Отладка в консоль
    await dp.start_polling(bot, skip_updates=True)

# ✅ Запуск бота
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
