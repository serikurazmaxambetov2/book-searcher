import asyncio
import logging

from bot.handlers import router
from bot.misc import bot, dp


async def main():
    # Подключаем логирование
    logging.basicConfig(level=logging.INFO)

    # Подключаем обработчики
    dp.include_router(router)

    # Запуск
    await dp.start_polling(bot)


asyncio.run(main())
