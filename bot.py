import asyncio
from misc import env
from handlers import start, help, menu
from aiogram import Bot, Dispatcher


async def main():
    bot = Bot(token=env.TgKeys.TOKEN)
    dp = Dispatcher()

    dp.include_routers(start.router, menu.router, help.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
