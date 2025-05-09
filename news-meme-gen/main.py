import asyncio
from config.config import bot, dp, loop, SMESHNYAVK_AI_ID, RIA_NOVOSTI, MIRRORING_TIMEOUT, PASSWORD, database
from keyboards.set_menu import set_main_menu
from handlers import other_handlers, news_handlers, rating_handlers
from middlewares import middlewares
import ria_mirroring_ugaralka.mainloop
from get_last_message import get_last_message
import logging

async def main() -> None:  
    logging.basicConfig(filename='logs/logs',
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO
                    )
    await bot.delete_webhook(drop_pending_updates = True)
    await set_main_menu(bot)
    dp.include_router(other_handlers.rt)
    dp.include_router(rating_handlers.rt)
    dp.include_router(news_handlers.rt)
    dp.update.middleware.register(middlewares.SaveChatIDMiddleware("db/database.json"))
    dp.update.middleware.register(middlewares.Auth(PASSWORD, database, False))
    mirroring = asyncio.create_task(ria_mirroring_ugaralka.mainloop.mainloop(SMESHNYAVK_AI_ID, RIA_NOVOSTI, MIRRORING_TIMEOUT))
    print("starting")
    main_polling = asyncio.create_task(dp.start_polling(bot))
    print(await asyncio.gather(main_polling, mirroring, return_exceptions=True))


if __name__ == "__main__":
    loop.run_until_complete(main())