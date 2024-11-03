from os import getenv

# Настройки бота
BOT_TOKEN = getenv("BOT_TOKEN", "")

# Настройки FSM
REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(getenv("REDIS_PORT", "6379"))

# Настройки backend
BACKEND_URL = getenv("BACKEND_URL", "http://localhost:3000")
