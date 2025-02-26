from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from core.postgres.access import get_async_session
from models.objects import ObjectModel


async def get_reports_kb():
    async for session in get_async_session():
        objects = await session.execute(
            select(ObjectModel.name)
        )
        objects = objects.scalars().all()
        keyboard = InlineKeyboardBuilder()
        for obj in objects:
            keyboard.row(
                InlineKeyboardButton(
                    text=str(obj),
                    callback_data="object_" + str(obj),
                )
            )

        return keyboard.as_markup()
