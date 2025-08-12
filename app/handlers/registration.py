from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from aiosqlite import connect
import app.config as cfg
import app.database as db
from re import fullmatch
router = Router()

class Reg(StatesGroup):
    name = State()
    kod = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    try:
        reg, role = await db.registration_check(message.from_user.id)
    except: 
        await message.answer(f"Ошибка проверки пользователя."); return

    if reg:
        await message.answer(f"Здравствуйте {message.from_user.first_name}!\nПохоже вы не проходили регистрацию, пожалуйста, выберите роль.", reply_markup=kb.main)
    elif reg and role:
        await message.answer(f"Здравствуйте {message.from_user.first_name}!", reply_markup=kb.start_teacher)
    elif reg and not role:
        await message.answer(f"Здравствуйте {message.from_user.first_name}!", reply_markup=kb.start_student)

#Регистрация студента
@router.callback_query(F.data == "student")
async def student(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Введите полное ФИО")
    await state.set_state(Reg.name)

@router.message(Reg.name)
async def all_name(message: Message, state: FSMContext):
    text = message.text
    if bool(fullmatch(r"[а-яА-Яa-zA-Z ]+", text)):
        await state.set_data(Reg.name, text)
        await message.answer("Введите код учителя")
        await state.set_state(Reg.kod)
    else: 
        await message.answer("Имя содержит недопустимые символы!")
        
@router.message(Reg.kod)
async def code(message: Message, state: FSMContext):
    try:
        kod = int(message.text)
    except:
        await message.answer("Код содержит недопустимые символы!")

    result = await db.check_kod(kod)
    name = await state.get_data(Reg.name)

    if result:
        try:
            await db.registration_student(kod, message.from_user.id, name)
        except: 
            await message.answer("Ошибка регистрации!")

        await message.answer("Вы успешно привязали себя к учителю!")
        await state.clear()
    else:
        await message.answer("Код не найден.")

#Регистрация учителя
@router.callback_query(F.data == "teacher")
async def student(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Введите полное ФИО")
    await state.set_state(Reg.name)

@router.message(Reg.name)
async def all_name(message: Message, state: FSMContext):
    text = message.text
    if bool(fullmatch(r"[а-яА-Яa-zA-Z ]+", text)):
        await db.registration_teacher(message.from_user.id, text)
        await message.answer("Ошибка регистрации!")
        await state.clear()
    else: 
        await message.answer("Имя содержит недопустимые символы!")
        
@router.message(Reg.kod)
async def code(message: Message, state: FSMContext):
    try:
        kod = int(message.text)
    except:
        await message.answer("Код содержит недопустимые символы!")

    result = await db.check_kod(kod)
    name = await state.get_data(Reg.name)

    if result:
        try:
            await db.registration_student(kod, message.from_user.id, name)
        except: 
            await message.answer("Ошибка регистрации!")

        await message.answer("Вы успешно привязали себя к учителю!")
        await state.clear()
    else:
        await message.answer("Код не найден.")