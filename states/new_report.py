from aiogram.fsm.state import State, StatesGroup


class NewReport(StatesGroup):
    choose_method = State()
    choose_name_for_object = State()
    send_photo = State()
