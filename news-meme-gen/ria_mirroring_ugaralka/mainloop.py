import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from config.config import bot, model, link_preview_options
from handlers.news_handlers import text_gen
from get_last_message import get_last_message
import asyncio
from uuid import uuid1
from aiogram.types.input_file import FSInputFile


async def mainloop(mirror_channel_id, source_channel_username, timeout=60*10):
    last_msg = None
    print("starting channel mirroring")
    while True:
        msg, media_path = await get_last_message(source_channel_username)
        if msg.text != last_msg:
            joke = await text_gen(msg.text, censor=True)
            if media_path:
                model.image_model.template_n = 3
                path = f"temp/{uuid1()}.jpg"
                model.image(media_path, path)
                await bot.send_photo(mirror_channel_id, FSInputFile(path), caption=joke)
                os.remove(path)
            else:
                await bot.send_message(mirror_channel_id, joke, link_preview_options=link_preview_options)
        last_msg = msg.text

        await asyncio.sleep(timeout)