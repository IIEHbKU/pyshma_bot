import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Здравствуйте, я помогу Вам следить за работой предприятия!", )


@router.message()
async def f(message: Message):
    await message.answer("Команда не распознана")
