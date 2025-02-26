import os

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from sqlalchemy import select, insert, update

from core.postgres.access import get_async_session
from keyboards.new_report import new_report_kb
from models.objects import ObjectModel
from states.new_report import NewReport
from utils.create_report import create_report

router = Router()


@router.message(F.text.lower() == 'добавить новый отчёт для объекта')
async def get_objects_with_new(message: Message, state: FSMContext):
    await message.answer("Выберите объект:", reply_markup=await new_report_kb())
    await state.set_state(NewReport.choose_object)


@router.callback_query(F.data == 'new_object', StateFilter(NewReport.choose_object))
async def get_objects(message: Message, state: FSMContext):
    await message.answer("Введите название нового объекта")
    await state.set_state(NewReport.choose_name_for_object)


@router.message(StateFilter(NewReport.choose_name_for_object), F.text)
async def new_object(message: Message, state: FSMContext):
    print(message.text)
    async for session in get_async_session():
        await session.execute(
            insert(ObjectModel).values(name=message.text),
        )
        await session.commit()
    await message.answer("Объект успешно добавлен!")
    await message.answer("Выберите объект:", reply_markup=await new_report_kb())
    await state.set_state(NewReport.choose_object)


@router.callback_query(F.data.startswith('object_'), StateFilter(NewReport.choose_object))
async def new_report(message: Message, state: FSMContext):
    print(message.data)
    object_name = message.data.split('_')[1]
    await state.update_data(object=object_name)
    await message.answer("Отправьте фото объекта")
    await state.set_state(NewReport.send_photo)


@router.message(F.photo, StateFilter(NewReport.send_photo))
async def send_photo(message: Message, state: FSMContext):
    await message.bot.download(file=message.photo[-1].file_id,
                               destination=f"./assets/{message.photo[-1].file_id}.jpg")
    data = await state.get_data()
    object_name = data.get('object')
    async for session in get_async_session():
        _id = await session.execute(
            select(ObjectModel.reports_count).where(ObjectModel.name == object_name)
        )
        _id = _id.scalars().all()
        _id = _id[0] + 1
        await session.execute(
            update(ObjectModel).where(ObjectModel.name == object_name).values(reports_count=_id)
        )
        await session.commit()
        res = await create_report(object_name, f"./assets/{message.photo[-1].file_id}.jpg", _id)
        filename_txt = res[0]
        filename_png = res[1]

        if filename_png is not None:
            await message.answer_document(FSInputFile(filename_png))
            os.remove(filename_png)
            os.remove(f"./assets/{message.photo[-1].file_id}.jpg")
        else:
            await message.answer_document(FSInputFile(f"./assets/{message.photo[-1].file_id}.jpg"))
            os.remove(f"./assets/{message.photo[-1].file_id}.jpg")

        await message.answer_document(FSInputFile(filename_txt))
        os.remove(filename_txt)

        await message.answer(f"Отчёт #{_id} успешно добавлен!")
        await state.clear()
