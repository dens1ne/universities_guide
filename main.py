from telebot import custom_filters

from bot_init import bot
from utils.set_bot_commands import set_default_commands
from handlers import *
from keyboards import *


if __name__ == "__main__":
    set_default_commands(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)
