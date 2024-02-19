from telebot.types import Message
from bot_init import bot
from states import SearchStates
from database.db_requests import short_name
from keyboards.search_olympiads import olymp_select_markup, calculate_or_add_markup


@bot.message_handler(state=SearchStates.get_olymp_name)
def search_olympiad(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        base_message: Message = data['start_message']
        result = short_name(data['selected_university'], message.text)
        if result:
            data['result'] = result
            bot.edit_message_text(text=f'Выбранный университет: {data["selected_university"]}\n'
                                        'Выберите один из предложенных вариантов:',
                                  chat_id=base_message.chat.id, message_id=base_message.message_id)
            bot.edit_message_reply_markup(base_message.chat.id,
                                          base_message.message_id,
                                          reply_markup=olymp_select_markup(result))
            bot.set_state(message.from_user.id, SearchStates.select_olymp, message.chat.id)
        else:
            bot.set_state(message.from_user.id, SearchStates.calculate_or_add, message.chat.id)
            bot.edit_message_text(text=f'Выбранный университет: {data["selected_university"]}\n'
                                       f'К сожалению, ничего не было найдено по запросу "{message.text}".\n'
                                       f'Выберите действие:',
                                  chat_id=base_message.chat.id, message_id=base_message.message_id,
                                  reply_markup=calculate_or_add_markup())
        bot.delete_message(message.chat.id, message.message_id)
