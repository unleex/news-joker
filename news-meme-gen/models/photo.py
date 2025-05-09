# Список заготовленных подписей
CAPTIONS = [
    "Это не баг, это фича",
    "Когда понял, что сегодня пятница",
    "Моя реакция на твои сообщения",
    "Я принял решение за тебя",
    # "Зацените мой Х*Й",
    "А я говорил, что так будет",
    # "Жизнь как зебра: то полоса,\n                    то занюхнул",
    "Чайник свистнул – пора курить",
    "Спасибо, я сам в шоке",
    "Лучше бы я спал",
    "Это не я, это мой дементор",
    "Когда забыл выключить утюг",
    "Моя душа после пятого кофе",
    "Типа я не в фокусе, типа арт",
    "Понедельник меня не догонит",
    "Шлёпнул бы, да рука устала",
    "Включил режим кактуса",
    "Смотрю в окно, вижу смысл жизни",
    "Мем-культура меня погубит",
    "Когда диплом за тебя говорит",
    "Я как этот стул",
    "Душ принял, теперь я бог",
    "Это не кринж, это искренне",
    "Моя аватарка в реальной жизни",
    "Пельмени спасут мир",
    "Я это сфоткал, я это выложил,\n                  я это удалю",
    "Жду сигнала из космоса",
    # "Мозг:404 Not Found",
    "Ваш текст здесь (но лучше не надо)",
    "Когда понял, что хлеб дороже любви",
    "Введите текст",
    
    "Я не кричу, я проектирую ауру",
    "Спасибо, я сам себя напугал",
    "Это не я",
    "'Завтра на диету'",
    "Когда WiFi сильнее любви",
    "Моя душа в режиме энергосбережения",
    "Фото сделано до того,\n как всё пошло не так",
    "Жду одобрения",
    "Выдыхаю в формате JPEG",
    "Это не тревога, это предвкушение",
    "Умный чел",
    "Смотрю в пустоту, пустота одобряет",
    "Ваше мнение сохранено в /dev/null",
    "Я за пивом",
    "Жизнь – это боль",
    "Улыбаюсь, чтобы скрыть \n вкладку с порно",
    "Волк в цирке не выступает",
    # "Я лох",
    "Пятница: попытка №327",
    "Селфи с будущим собой \n (он не в восторге)",
    "Думаю о тебе... то есть ни о чём",
    "Я",
    "Стол",
    "Стул",
    # "Пошел на*уй"
]

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import random
from io import BytesIO



def download_image(path):
    """Скачивание изображения по URL"""
    return Image.open(path).convert("RGB")

def add_random_caption(image):
    """Добавление случайной подписи на изображение"""
    size = image.size
    if size[0]>size[1]:
        new_size= (1220,1080)
    else:
        new_size=(1080,1220)
    image = image.resize(new_size)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("font/ARIAL.TTF", 60)
    
        
    caption = random.choice(CAPTIONS)
    text_bbox = draw.textbbox((0, 0), caption, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (image.width - text_width) // 2
    y = image.height - text_height - 30
    
    # Добавляем фон для текста
    
    draw.text((x, y), caption, font=font, fill="white")
    return image

def process_template2(image):
    """Обработка по второму шаблону"""
    new_size = (800, 800)
    image = image.resize(new_size)
    size = max(image.size)
    framed_image = ImageOps.pad(image, (size, size), color="white", centering=(0.5, 0.5))
    
    # Добавляем внешнюю рамку
    bordered_image = ImageOps.expand(framed_image, border=2, fill="white")
    # Создаем квадрат с рамкой
    size = max(image.size)
    framed_image = ImageOps.pad(bordered_image, (size, size), color="black", centering=(0.5, 0.5))
    
    # Добавляем внешнюю рамку
    result = ImageOps.expand(framed_image, border=100, fill="black")

    draw = ImageDraw.Draw(result)

    font = ImageFont.truetype("font/ARIAL.TTF", 40)
    
    caption = random.choice(CAPTIONS)
    text_bbox = draw.textbbox((0, 0), caption, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (result.width - text_width) // 2
    y = result.height - text_height - 30
    
    # Добавляем фон для текста
    draw.rectangle(
        [x - 10, y - 10, x + text_width + 10, y + text_height + 10],
        fill="black"
    )
    draw.text((x, y), caption, font=font, fill="white")
    return result

def degrade_quality(image):
    """Ухудшение качества изображения"""
    # Применяем размытие и снижаем качество
    size = image.size
    if size[0]>size[1]:
        new_size= (1220,1080)
    else:
        new_size=(1080,1220)
    image = image.resize(new_size)
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=1)
    buffer.seek(0)
    return Image.open(buffer)

def process_image(image_path, template):
    """Основная функция обработки"""
    image = download_image(image_path)
    
    if template == 1:
        result = add_random_caption(image)
    elif template == 2:
        result = process_template2(image)
    elif template == 3:
        image = add_random_caption(image)
        result = degrade_quality(image)
    else:
        raise ValueError("Неверный номер шаблона")
    
    return result


class PhotoModel:
    
    def __init__(self, template_n):
        self.template_n = template_n

    def __call__(self, initial_image_path, generated_image_path):
        gen = process_image(initial_image_path, self.template_n)
        gen.save(generated_image_path)