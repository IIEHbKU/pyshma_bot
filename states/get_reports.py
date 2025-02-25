from aiogram.fsm.state import State, StatesGroup


class GetReports(StatesGroup):
    get_reports_by_object = State()
