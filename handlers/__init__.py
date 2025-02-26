from aiogram import Dispatcher

from handlers.default import router as default_router
from handlers.get_reports import router as get_reports_router
from handlers.new_report import router as new_report_router
from handlers.error import router as error_router


def include_routers(dp: Dispatcher):
    dp.include_routers(get_reports_router)
    dp.include_routers(new_report_router)
    dp.include_routers(default_router)
    dp.include_routers(error_router)
