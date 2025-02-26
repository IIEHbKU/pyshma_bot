from aiogram.fsm.state import State, StatesGroup


class NewReport(StatesGroup):
    choose_object = State()
    choose_name_for_object = State()
    send_photo = State()
