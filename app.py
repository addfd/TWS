import asyncio

from aiogram import Bot, Dispatcher, types

from middlewares.db import DataBaseSession

from database.engine import create_db, drop_db, session_maker

from handlers.user import user_private_router
from handlers.admin import admin_router

from common.bot_cmds_list import private



bot = Bot("6628638875:AAHWKt84Qu7wrPEEBcauEIh425jODdsUND8")  # БОТ
bot.my_admins_list = {}

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(admin_router)

async def on_startup():

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown():
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())
