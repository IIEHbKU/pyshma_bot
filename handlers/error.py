from aiogram import Router
from aiogram.types import CallbackQuery, Message

router = Router()


@router.callback_query(lambda callback_query: True)
async def handle_invalid_state(callback_query: CallbackQuery):
    await callback_query.answer("Невозможно выполнить действие в текущем состоянии!", show_alert=True)


@router.message()
async def f(message: Message):
    await message.answer("Невозможно выполнить действие в текущем состоянии!")
