from aiogram.types import BotCommand
from aiogram import Bot


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command="start", description="Запуск"),
        BotCommand(command="help_admin", description="Список команд для админов"),
        BotCommand(command="rate", description="Оценить шутки и поднять карму"),
        BotCommand(command="censor", description="Включить/выключить цензуру"),
        BotCommand(command="auth", description="Авторизация"),
        ]
    await bot.set_my_commands(main_menu_commands)