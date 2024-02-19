from bot_init import bot
from telebot.types import Message
from states import SearchStates
from keyboards.select_university import unv_markup


@bot.message_handler(commands=['start'])
def start_search(message: Message):
    bot.set_state(message.from_user.id, SearchStates.select_universities, message.chat.id)
    bot.send_message(message.chat.id, 'Выберите один из предложенных университетов', reply_markup=unv_markup())

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['selected_university'] = None
        data['selected_olymp'] = None
        data['start_message'] = None
        data['result'] = list()
        data['confirmed'] = dict()
