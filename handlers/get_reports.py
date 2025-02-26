import os

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from natsort import natsorted

from core.minio.access import get_minio
from core.settings import settings
from keyboards.get_reports import get_reports_kb
from states.get_reports import GetReports

router = Router()


@router.message(F.text.lower() == 'получить отчёты об объекте')
async def choose_object(message: Message, state: FSMContext):
    await message.answer("Выберите объект:", reply_markup=await get_reports_kb())
    await state.set_state(GetReports.choose_object)


@router.callback_query(F.data.startswith('object_'), StateFilter(GetReports.choose_object))
async def get_reports(callback_query: CallbackQuery, state: FSMContext):
    object_name = callback_query.data.split('_')[1]
    folder = f"{object_name}/"
    await callback_query.message.answer(f"Отчёты по объекту [{object_name}]:")

    minio_client = await get_minio()
    objects = minio_client.list_objects(settings.minio_bucket, prefix=folder, recursive=True)

    sorted_objects = natsorted(objects, key=lambda _obj: _obj.object_name)

    ll = 0
    rep = 0
    for obj in sorted_objects:
        ll += 1
        file_path = obj.object_name
        if ll % 2 != 0:
            rep += 1
            await callback_query.message.answer(f"Отчёт #{rep}:")
        await send_file(callback_query.message, file_path, minio_client)

    await state.clear()


async def send_file(message: Message, file_path, minio_client):
    file_data = minio_client.get_object(settings.minio_bucket, file_path)
    file_name = os.path.basename(file_path)

    with open(file_name, 'wb') as f:
        for d in file_data.stream(32 * 1024):
            f.write(d)

    await message.answer_document(FSInputFile(file_name))
    os.remove(file_name)
