import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_init import bot
from config import universities
from states import SearchStates
from .search_olympiads import calculate_or_add_markup


def unv_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(*(InlineKeyboardButton(univ, callback_data=univ) for univ in universities))
    return markup


@bot.callback_query_handler(func=lambda call: True, state=SearchStates.select_universities)
def university_callback_query(call: telebot.types.CallbackQuery):
    message = call.message
    print(call.from_user.id, message.chat.id)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text=f'Выбран университет: {call.data}\nВыберите действие:')
    bot.set_state(call.from_user.id, SearchStates.calculate_or_add, message.chat.id)
    bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=calculate_or_add_markup())
    with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
        data['selected_university'] = call.data
        data['start_message'] = message
