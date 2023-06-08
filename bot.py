import asyncio
from misc import env
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import start, help, menu
from aiogram import Bot, Dispatcher
from misc.utils import birthday_sending


async def main():
    bot = Bot(token=env.TgKeys.TOKEN)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()
    dp.include_routers(start.router, menu.router, help.router)
    scheduler.add_job(birthday_sending, trigger="cron", hour="10", minute="00", args=(bot,))
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
