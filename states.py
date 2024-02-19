from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    select_universities = State()
    calculate_or_add = State()
    get_olymp_name = State()
    select_olymp = State()
    confirm_adding = State()
    calculate_result = State()
