import logging
import os

# ✅ Определяем уровень логирования (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# ✅ Создаем глобальный логгер
logging.basicConfig(
    filename="debug.log",  # ✅ Записываем в `debug.log`
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# ✅ Логируем, что логгер загружен
logger.info("✅ Логгер успешно инициализирован!")
