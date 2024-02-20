import telebot
from telebot.types import BotCommand
from config import DEFAULT_COMMANDS


def set_default_commands(bot: telebot.TeleBot):
    print(DEFAULT_COMMANDS)
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])
