import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.config import SMESHNYAVK_AI_CHATNAME

def joke_added(topic, jokes):
    ret = f"Добавлены прикольчики на тему {topic}\n"
    for idx, joke in enumerate(jokes):
        ret += f"{idx + 1}. {joke}"
    return ret


LEXICON_RU = {
    "else_handler": "Не понимаю",
    "other_phrase": "Aiogram rocks!",
    "start": """
Привет👋! Сразу кидай свою новость: фото, пост, голосовое, давай, напридумываю тебе всякого!✨
⚠️Внимание, в боте включена цензура неполиткорректных ответов. Чтобы ее включить/выключить, отправьте /censor
""",
    "add_joke/init": "пришли тему шутки",
    "add_joke/joke": "присылай шутки. когда надоест, высри /done",
    "help_admin":
    """
/add_joke - Добавить шутку в бота""",
"rate_joke": "Как тебе?",
"rating_ended": "Учту, спасибо!!",
"text_preloader": "💬Думаем...",
"model_answer": f'❗️%s\n\n<i><a href="t.me/{SMESHNYAVK_AI_CHATNAME}"> Смешнявк-AI. Подписаться.</a></i>',
"censored": '💀\n<span class="tg-spoiler">%s</span>"',
'select_meme_style': 'selecto varianto de brainroto: 1 2 3',
"rating_joke": """
Тема: 
%s

Шутка:
%s
""",
'already_rated_everything': "Все шутки размечены! Спасибо тебе большое!!!",
'started_rating':
'''Я тебе буду кидать шутки, а ты оценивай их от 1 до 10. Если захочешь перестать, отправь /stop_rating
p.s. если сообщение кривое с шуткой и заголовком дважды, не обращай внимания, это проблемка датасета:3 исправляем!
''',
'rating_stopped': """Спасибо тебе!!!""",
'censorship_on': 'Цензура включена.',
'censorship_off': 'Цензура выключена.',
'blocked': '❌Неполиткорректный ответ заблокирован! Попробуете еще раз?',
'unauthorized': "Извините, вы не прошли авторизацию, или пароль неверный. Для установки пароля, если он у вас есть, хехе, введите /auth [пароль]",
'password_set': "Пароль установлен"
    }