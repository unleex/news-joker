#!/usr/bin/env python3

import argparse

from config.config import telethon_client, db_connection
from uuid import uuid1
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument


DEFAULT_OUTPUT_PATH = 'last_message_from_channel.txt'
parser = argparse.ArgumentParser()

async def get_last_message(target_group=None):
    if target_group and target_group.startswith('@'):
        target_group = target_group.split('@')[1]
    async for msg in telethon_client.iter_messages(target_group, limit=1):
        last_message = msg
    photo_path = None
    if msg.media and isinstance(msg.media, MessageMediaPhoto):
        photo_path = await telethon_client.download_media(last_message.media)
    return last_message, photo_path