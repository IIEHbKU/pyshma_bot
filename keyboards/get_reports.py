from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.postgres.access import get_async_session


async def get_reports():
    db_session = get_async_session

    async with db_session() as session:
        reports = await session.execute(
            "SELECT id, name FROM objects",
        ).fetchall()

    keyboard = InlineKeyboardMarkup()
    for report in reports:
        keyboard.add(
            InlineKeyboardButton(
                text=str(report[1]),
                callback_data="report_" + str(report[0]),
            )
        )

    return keyboard
