from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from . import config

# Настройки хранилища
key_builder = DefaultKeyBuilder(with_destiny=True)
redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
storage = RedisStorage(redis=redis, key_builder=key_builder)

# Настройки бота и dp
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(storage=storage)
