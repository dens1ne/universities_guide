from telebot.types import Message
from bot_init import bot


@bot.message_handler(state="*")
def clean(message: Message):
    bot.delete_message(message.chat.id, message.message_id)
