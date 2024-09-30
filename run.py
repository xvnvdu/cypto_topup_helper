from aiogram import Bot, Dispatcher
from handlers import router
from hiden import bot_token


bot = Bot(bot_token)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=False)

if __name__ == '__main__':
    import asyncio
    print('Начало работы...')
    asyncio.run(main())

