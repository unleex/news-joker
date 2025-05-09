import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import json
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import *
import logging
import typing
from lexicon.lexicon import LEXICON_RU as lexicon
from handlers.other_handlers import auth
from config.config import bot

logger = logging.getLogger(__name__)

class SaveChatIDMiddleware(BaseMiddleware):

    def __init__(self, db_file="database.json"):

        super().__init__()
        self.db_file = db_file


    def save_chat_id(self, chat_id, initial_data: dict = {}):
        try:
            # Load existing data
            with open(self.db_file, "r") as file:
                data = json.load(file)
            # Add chat_id if not already present
            if str(chat_id) not in data["users"]:
                data['users'][chat_id] = initial_data

            # Save updated data
            with open(self.db_file, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"Error saving chat_id: {e}")
        
    
    async def on_pre_process_update(self, update: Update, data: dict):
        user_id = None
        update_data: CallbackQuery | Message | None = None
        if update.message:
            update_data = update.message
        elif update.callback_query:
            update_data = update.callback_query
        elif update.channel_post:
            update_data = update.channel_post

        if update_data is not None:
            user_id = update_data.from_user.id
            self.save_chat_id(user_id, initial_data={"username": update_data.from_user.username, 'censorship_on': True})
        else:
            logger.error(f"No chat id found for {update}")

    
    async def __call__(
        self,
        handler: typing.Callable[[TelegramObject, typing.Dict[str,  typing.Any]], typing.Awaitable[ typing.Any]],
        event: TelegramObject,
        data:  typing.Dict[str,  typing.Any]
    ) ->  typing.Any:
        await self.on_pre_process_update(event, data) # type: ignore
        return await handler(event, data)


async def unauthorized_handler(userid):
    await bot.send_message(userid, lexicon['unauthorized'])


class Auth(BaseMiddleware):

    def __init__(self, password: str, db, enabled=True):
        self.password = password
        self.db = db
        self.enabled = enabled
    
    async def __call__(
        self,
        handler: typing.Callable[[TelegramObject, typing.Dict[str,  typing.Any]], typing.Awaitable[ typing.Any]],
        event: TelegramObject,
        data:  typing.Dict[str,  typing.Any]
    ) ->  typing.Any:
        userid = str(data['event_from_user'].id)
        db_user_data = self.db['users'][userid]
        if hasattr(event, 'message') and event.message.text is not None and event.message.text.startswith('/auth'):
            await auth(event.message)
            return
        if not self.enabled or ('password' in db_user_data and db_user_data['password'] == self.password):
            return await handler(event, data)
        else:
            return await unauthorized_handler(userid)