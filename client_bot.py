import os
import asyncio

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from handlers.client_handlers import authorization

load_dotenv()


async def main():
    bot = Bot(token=os.getenv('CLIENT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(authorization.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())