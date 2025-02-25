from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_kb():
    kb = [
        [KeyboardButton(text="Добавить новый отчёт для объекта")]
        [KeyboardButton(text="Получить отчет об объекте")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def cancel_kb():
    kb = [
        [KeyboardButton(text="Отмена")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
