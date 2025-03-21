import os
import logging

# Настраиваем логирование для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем токен бота
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ Ошибка: TELEGRAM_TOKEN не найден!")
    exit(1)

# Загружаем ссылки из переменных окружения (названия из Vercel)
GAME_URL = os.getenv("GAME_URL", "https://clicker-geminy.vercel.app/rocket-game.html")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://clicker-pi-two.vercel.app/")

# Выводим ссылки в логи, чтобы проверить корректность
logger.info(f"✅ TELEGRAM_TOKEN загружен: {BOT_TOKEN[:10]}********")
logger.info(f"✅ GAME_URL: {GAME_URL}")
logger.info(f"✅ WEBAPP_URL: {WEBAPP_URL}")
