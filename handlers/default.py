from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.default import start_kb

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Здравствуйте, я помогу Вам следить за работой предприятия!", reply_markup=start_kb())
