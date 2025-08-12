from aiosqlite import connect

#Проверка на регистрацию и роль в системе
async def registration_check(id):
    async with connect('database.db') as db:
        # Проверка среди учителей
        async with db.execute('SELECT id FROM Teachers WHERE telegram_id = ?', (id,)) as cursor:
            teacher = await cursor.fetchone()
            if teacher:
                return True, True  # зарегистрирован, role = teacher (True)

        # Проверка среди учеников
        async with db.execute('SELECT id FROM Students WHERE telegram_id = ?', (id,)) as cursor:
            student = await cursor.fetchone()
            if student:
                return True, False  # зарегистрирован, role = student (False)

        #Если не зарегистрирован
        return False, False

#Проверка доступных заданий от учителя для ученика
async def assignments_check(id):
    async with connect("database.db") as db:
        async with db.execute(f"SELECT assignments FROM Stedents WHERE telegram_id = {id}") as cursor:
            cursor = cursor.fetchall()
            return cursor 
        
#Проверка доступных заданий которые задавал учитель
async def assignments_check_teacher(id):
    async with connect("database.db") as db:
        async with db.execute(f"SELECT assignments FROM Stedents WHERE teacher_id = {id}") as cursor:
            cursor = cursor.fetchall()
            return cursor 

#Регистрация студента в базу данных
async def registration_student(kod, id, name):
    async with connect("database.db") as db:
        await db.execute("INSERT INTO Students (teacher_id, telegram_id, name)", (kod, id, name))
        await db.commit()

#Регистрация учителя в базу данных
async def registration_teacher(id, name):
    async with connect("database.db") as db:
        await db.execute("INSERT INTO Teachers (telegram_id, name)", (id, name))
        await db.commit()

#Проверка кода от ученика, для поиска учителя.
async def check_kod(kod):
    async with connect('database.db') as db:
        async with db.execute('SELECT id FROM Teachers WHERE telegram_id = ?', (kod,)) as cursor:
            return bool(cursor)
        
#Проверка кода викторины
async def check_kode_quiz(kod, id):
    async with connect('database.db') as db:
        async with db.execute('SELECT id FROM Teachers WHERE telegram_id = ?', (kod,)) as cursor:
            return bool(cursor)
              
                