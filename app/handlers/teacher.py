from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from aiosqlite import connect
import app.config as cfg
import app.database as db

teacher_router = Router()

class Assignments(StatesGroup):
    name = State()
    image = State()
    content = State()
    
@teacher_router.callback_query(F.data == "assignments")
async def assignments(callback: CallbackQuery, state: FSMContext):
    result = await db.assignments_check_teacher(callback.from_user.id)
    text = ""
    for key, value in result.items():
        text += f"\n{value}. {key}"
    await callback.message.answer(f"Список заданных вами заданий:{text}", reply_markup=kb.assign_settings)

@teacher_router.callback_query(F.data == "assignments_new")
async def assignments_new(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Введите название нового задания")
    await state.set_state(Assignments.name)

@teacher_router.message(Assignments.name)
async def assignments_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Хотите прекрипить изображение?", reply_markup=kb.image_connect)

@teacher_router.callback_query(F.data == "image_yes")
async def assignments_new(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Assignments.image)
    await callback.answer("Отправте изображение которое хотите прекрипить")

@teacher_router.callback_query(F.data == "image_no")
async def assignments_new(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Assignments.content)
    await callback.answer("Отправте задание.\nЗадание может содержать файлы, картинки голосовые сообщения или текст")
