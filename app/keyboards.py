from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main = ReplyKeyboardMarkup(inline_keyboard=[[KeyboardButton(text="Ученик", callback_data="student")],
                                             [KeyboardButton(text="Учитель", callback_data="teacher")]])

start_student = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Задания", callback_data="assignments")], 
                                              [InlineKeyboardButton(text="Вход в викторину", callback_data="quiz_entrance")],
                                              [InlineKeyboardButton(text="Рейтинг", callback_data="top")],
                                              [InlineKeyboardButton(text="Профиль класса", callback_data="class_profiles")]])

start_teacher = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Задания", callback_data="assignments")],
                                              [InlineKeyboardButton(text="Режим викторины", callback_data="quiz")],
                                              [InlineKeyboardButton(text="Просмотр класса", callback_data="profile_class")]])

student_quiz_no_teacher = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да", callback_data="quiz_yes")], 
                                              [InlineKeyboardButton(text="Нет", callback_data="quiz_no")]])

assign_settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Новое задание", callback_data="assignments_new")],
                                                        [InlineKeyboardButton(text="Редактор заданий", callback_data="assignments_settigns")]])

image_connect = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да", callback_data="image_yes")], 
                                              [InlineKeyboardButton(text="Нет", callback_data="image_no")]])

markup = ReplyKeyboardRemove()
