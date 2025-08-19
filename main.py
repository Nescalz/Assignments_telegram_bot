import asyncio
from aiogram import Bot, Dispatcher, F
from sqlite3 import connect
from app.config import token

from app.handlers.registration import router
from app.handlers.teacher import teacher_router
from app.handlers.student import student_router

connectdb = connect("database.db")
cursor = connectdb.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    role BOOLIAN
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    assignments TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_teacher INTEGER NOT NULL,
    id_student TEXT NOT NULL,
    name TEXT NOT NULL
)
''')

connectdb.commit()
connectdb.close()

async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(teacher_router)
    dp.include_router(student_router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("off")
