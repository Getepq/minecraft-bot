import asyncio

from aiogram import Bot ,Dispatcher
from handl.user_hand import rt as usr_hand
from handl.admin_hand import rt as admin_hand
from db.dbMod import create_db
import os

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_router(usr_hand)
dp.include_router(admin_hand)

async def main():
    await create_db()
    print('DB created')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Goodbye')








