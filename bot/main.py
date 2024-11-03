import asyncio
import logging

from aiogram_dialog import setup_dialogs

from bot.dialogs import dialog_register
from bot.handlers import router
from bot.misc import bot, dp


async def main():
    # Подключаем логирование
    logging.basicConfig(level=logging.INFO)

    # Подключаем обработчики
    dp.include_router(router)

    # Подключение диалога к dp
    dp.include_router(dialog_register)

    # Setup диалогов
    setup_dialogs(dp)

    # Запуск
    await dp.start_polling(bot)


asyncio.run(main())
