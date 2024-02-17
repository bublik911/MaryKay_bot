import os
import asyncio
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.consult_handlers import start, menu, check_clients, add_client, sending, delete_client, help
from aiogram import Bot, Dispatcher
from misc.utils import birthday_sending

load_dotenv()


async def main():
    consult_bot = Bot(token=os.getenv('CONSULT_TOKEN'))
    client_bot = Bot(token=os.getenv('CLIENT_TOKEN'))

    dp = Dispatcher()
    dp.include_routers(start.router, menu.router, help.router,
                       check_clients.router, add_client.router, sending.router,
                       delete_client.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(birthday_sending, trigger="cron", hour="19", minute="05", args=(consult_bot, client_bot, ))
    scheduler.start()

    await consult_bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(consult_bot)


if __name__ == "__main__":
    asyncio.run(main())
