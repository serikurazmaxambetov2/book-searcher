import asyncio

from bot.misc import bot, dp


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
