from aiogram.fsm.state import State, StatesGroup


class GetReports(StatesGroup):
    choose_object = State()
