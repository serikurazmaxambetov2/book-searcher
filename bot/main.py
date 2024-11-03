import asyncio
import logging

from bot.misc import bot, dp


async def main():
    # Подключаем логирование
    logging.basicConfig(level=logging.INFO)

    # Запуск
    await dp.start_polling(bot)


asyncio.run(main())
