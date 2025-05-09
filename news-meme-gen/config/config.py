import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, Redis
from environs import Env
import models.interface, models.audio, models.photo, models.text

from prompts.prompts import PROMPTS_RU as prompts
from database.database import Database
import random
import sqlite3
import saiga_def
import requests, zipfile, io
import telethon
from telethon import sync  # this module must be imported, although never used
from telethon.tl import functions, types
import asyncio
import asyncio
from aiogram.types.link_preview_options import LinkPreviewOptions

link_preview_options = LinkPreviewOptions(is_disabled=True)

loop = asyncio.new_event_loop()  # Create once and reuse
asyncio.set_event_loop(loop)
env: Env = Env()
env.read_env(override=True, recurse=False)
PASSWORD = env('PASSWORD')
db_connection = sqlite3.connect(env('DB_NAME'), check_same_thread=True)

cursor = db_connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS 'group' ("
    "'id' INTEGER PRIMARY KEY,"
    "'group_id' TEXT,"
    "'group_name' TEXT,"
    "'group_title' TEXT,"
    "'user_count' INTEGER)"
)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS 'user' ("
    "id INTEGER PRIMARY KEY,"
    "user_id TEXT,"
    "is_bot BOOLEAN,"
    "name TEXT,"
    "username TEXT)"
)

db_connection.commit()
db_connection.close()
try:
    telethon_client = telethon.TelegramClient(
        env('SESSION_NAME'), env('APP_API_ID'), env('APP_API_HASH'), loop=loop
        )
except Exception as e:
    print('Error while authenticating the user:\n\t%s' % e)
    sys.exit()

telethon_client.start(
    phone=env('TG_PHONE_NUMBER'),
    password=env('TG_PASSWORD'),
)

SMESHNYAVK_AI_ID = -1002502278781
SMESHNYAVK_AI_CHATNAME = "@aiugaralkaxaxa".replace('@','')
# SMESHNYAVK_AI_ID = -1002555090997
# SMESHNYAVK_AI_CHATNAME = "@ahahfbakfabfka"
RIA_NOVOSTI = "@rian_ru"


MIRRORING_TIMEOUT = 60*5

BOT_TOKEN = env('BOT_TOKEN').replace(r'\x3a',':')
ADMIN_IDS: list = list(map(int,env.list('ADMIN_IDS')))
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
redis = Redis(host='localhost', port=6380)
storage = RedisStorage(redis=redis) 
dp = Dispatcher(storage=storage)
# gpt = text.GPT(
#         system_prompt=prompts["system_news_meme_gen"]
#     )
# gpt = lambda x: "прикол?\n"+''.join([chr(random.randint(1,5000)) for _ in range(200)])
gpt = saiga_def.summarized_saiga
model = models.interface.NaebNet(
    text_model=gpt,
    audio_model=models.audio.STTGPT(
        stt=models.audio.SpeechModel(),
        gpt=gpt
    ),
    image_model=models.photo.PhotoModel(3)
)
database = Database(json_file='db/database.json', default_data={"users": {}, "jokes": []})
rated_jokes = Database('db/rated_jokes.json', default_data={})

if not os.path.exists('font'):
    url = 'https://font.download/dl/font/arial.zip'
    r = requests.get(url)
    with r, zipfile.ZipFile(io.BytesIO(r.content)) as archive:
        archive.extractall('font')