from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def new_report():
    kb = [
        [KeyboardButton(text="Добавить отчёт в новый объект")],
        [KeyboardButton(text="Отмена")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
