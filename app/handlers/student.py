from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import app.config as cfg
import app.database as db

student_router = Router()

class InQuiz(StatesGroup):
    kode = State()

def make_storage_quiz(): #Функция замыкания для хранения заданий квиза
    storage = {}

    def set_value(key, value, user_id):
        storage[(user_id, key)] = value  

    def get_value(key, user_id):
        return storage.get((user_id, key))  

    return set_value, get_value


set_value_storage, get_storage = make_storage_quiz()


@student_router.callback_query(F.data == "assignments")
async def assig(callback: CallbackQuery, state: FSMContext):
    assign = await db.assignments_check(callback.from_user.id)
    text = ""
    for assig, i in assign:
        text += f"\n{i}. {assig}"

    await callback.answer(f"Список доступных заданий для вас:{text}")

@student_router.callback_query(F.data == "quiz_entrance")
async def quiz_entrance(callback: CallbackQuery, state: FSMContext):
    await state.set_state(InQuiz.kode)
    await callback.answer("Введите код для входа")

@student_router.message(InQuiz.kode)
async def quiz_kode(message: Message, state: FSMContext):
    kode = message.text
    result = db.check_kode_quiz(kode, message.from_user.id)
    if result: #Код от учителя
        await message.answer("Код активирован! Ожидайте вопросов.")
        await state.clear()
    elif not result:
        await message.answer("Такой код существует, но создал его не ваш учитель.\nХотите продолжить?", reply_markup=kb.student_quiz_no_teacher)
        await state.clear()
    elif result == None:
        await message.answer("Такой код не существует. ")
        await state.clear()

@student_router.callback_query(F.data == "quiz_yes")
async def quiz_yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Код активирован! Ожидайте вопросов.")

@student_router.callback_query(F.data == "quiz_no")
async def quiz_yes(callback: CallbackQuery):
    await callback.message.delete()


