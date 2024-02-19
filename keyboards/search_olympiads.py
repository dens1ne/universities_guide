import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_init import bot
from database.db_requests import type_of_comp, conditions, bonuses
from states import SearchStates


def olymp_select_markup(olympiads: list):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        *(
            InlineKeyboardButton(olymp[0], callback_data=olymp[0])
            for olymp in olympiads
        ),
        InlineKeyboardButton("<--", callback_data="back"),
    )
    return markup


def confirm_select_olymp_markup(bonuses):
    degrs = ["участник", "призер", "победитель"]
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        *[
            InlineKeyboardButton(degrs[index], callback_data=degrs[index])
            for index, bonus in enumerate(bonuses)
            if bonus
        ],
        InlineKeyboardButton("<--", callback_data="back"),
    )
    return markup


def calculate_or_add_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Добавить олимпиаду", callback_data="add_olymp"),
        InlineKeyboardButton("Подсчитать баллы", callback_data="calculate"),
    )
    return markup


def start_message(call):
    message = call.message
    with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
        if data["confirmed"]:
            bot.set_state(
                call.from_user.id, SearchStates.calculate_or_add, message.chat.id
            )
            bot.edit_message_text(
                text="Выбранный университет: {university}\n\n"
                "Выбранные олимпиады: \n{olymps}\n\n"
                "Выберите действие:".format(
                    university=data["selected_university"],
                    olymps="\n".join(
                        [
                            f"{olymp_name} - {olymp_bonus[0]}, {olymp_bonus[1]} балл(-ов)"
                            for olymp_name, olymp_bonus in data["confirmed"].items()
                        ]
                    ),
                ),
                chat_id=message.chat.id,
                message_id=message.message_id,
            )
            bot.edit_message_reply_markup(
                message.chat.id,
                message.message_id,
                reply_markup=calculate_or_add_markup(),
            )
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=f"Выбран университет: {data['selected_university']}\nВыберите действие:",
            )
            bot.set_state(
                call.from_user.id, SearchStates.calculate_or_add, message.chat.id
            )
            bot.edit_message_reply_markup(
                message.chat.id,
                message.message_id,
                reply_markup=calculate_or_add_markup(),
            )


@bot.callback_query_handler(func=lambda call: True, state=SearchStates.calculate_or_add)
def next_move(call: telebot.types.CallbackQuery):
    if call.data == "add_olymp":
        message = call.message
        with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
            bot.edit_message_text(
                f'Выбран университет: {data["selected_university"]}\nНапишите название олимпиады:',
                message.chat.id,
                message.message_id,
            )
            bot.set_state(call.from_user.id, SearchStates.get_olymp_name)
    elif call.data == "calculate":
        message = call.message
        with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
            print(data["confirmed"])
            bot.edit_message_text(
                "Выбран университет: {university}\n"
                "Суммарное количество бонусных баллов: {bonus} из 10\n\n"
                "Чтобы заново подсчитать баллы, введите команду /start".format(
                    university=data["selected_university"],
                    bonus=sum(int(value[1]) for value in data["confirmed"].values()),
                ),
                chat_id=message.chat.id,
                message_id=message.message_id,
            )


@bot.callback_query_handler(func=lambda call: True, state=SearchStates.select_olymp)
def confirm(call: telebot.types.CallbackQuery):
    message = call.message
    with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
        if call.data != "back":
            data["selected_olymp"] = call.data
            bonus = bonuses(data["selected_university"], call.data)
            bot.edit_message_text(
                text=f'Выбран университет: {data["selected_university"]}\nВыбрана олимпиада "{call.data}"\n\n'
                f'<b>Условие:</b> {type_of_comp(data["selected_university"], call.data)[0]}\n\n'
                f'<b>Доп. условия:</b> {conditions(data["selected_university"], call.data)[0]}\n\n'
                + "{participant}{prewinner}{winner}".format(
                    participant=f"Участник: {bonus[0]}\n" if bonus[0] else "",
                    prewinner=f"Призёр: {bonus[1]}\n" if bonus[1] else "",
                    winner=f"Победитель: {bonus[2]}\n" if bonus[2] else "",
                ),
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode="HTML",
            )
            bot.edit_message_reply_markup(
                message.chat.id,
                message.message_id,
                reply_markup=confirm_select_olymp_markup(bonus),
            )
            bot.set_state(
                call.from_user.id, SearchStates.confirm_adding, message.chat.id
            )
        else:
            start_message(call)


@bot.callback_query_handler(func=lambda call: True, state=SearchStates.confirm_adding)
def after_confirm(call: telebot.types.CallbackQuery):
    degrs = ["участник", "призер", "победитель"]
    message = call.message
    with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
        bonus = bonuses(data["selected_university"], data["selected_olymp"])
        if call.data == degrs[0]:
            data["confirmed"][data["selected_olymp"]] = (degrs[0], bonus[0])
        elif call.data == degrs[1]:
            data["confirmed"][data["selected_olymp"]] = (degrs[1], bonus[1])
        elif call.data == degrs[2]:
            data["confirmed"][data["selected_olymp"]] = (degrs[2], bonus[2])

        if call.data == "back":
            base_message = data["start_message"]
            bot.edit_message_text(
                text=f'Выбранный университет: {data["selected_university"]}\n'
                "Выберите один из предложенных вариантов:",
                chat_id=base_message.chat.id,
                message_id=base_message.message_id,
            )
            bot.edit_message_reply_markup(
                base_message.chat.id,
                base_message.message_id,
                reply_markup=olymp_select_markup(data["result"]),
            )
            bot.set_state(call.from_user.id, SearchStates.select_olymp, message.chat.id)
        else:
            start_message(call)
