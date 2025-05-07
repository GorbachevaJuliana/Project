import asyncio
import os
import random
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
API_TOKEN = '8003685426:AAGbaa-jzCyNoHPCLA-kZE8Ilq3WrVPyb5o'

conn = sqlite3.connect('project_db.db')
cursor = conn.cursor()

class Form(StatesGroup):
    name = State()
    rating = State()
    age = State()
    country = State()
# gender_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='Мальчик')],
#         [KeyboardButton(text='Девочка')]
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True
# )
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    answers = ['Привет, как зовут игрока?', 'Введи имя игрока']
    await message.answer(random.choice(answers))
    await state.set_state(Form.name)

async def name_chose(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введи рейтинг игрока')
    await state.set_state(Form.rating)

async def rating_chose(message: Message, state: FSMContext):
    await state.update_data(rating=message.text)
    await message.answer('Сколько ему лет?')
    await state.set_state(Form.age)

async def age_chose(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Из какой он страны?')
    await state.set_state(Form.country)

async def country_chose(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    data = await state.get_data()
    await message.answer(f"Твои данные {data}")
    cursor.executemany('''
        INSERT INTO player (name, rating, age, country)
        VALUES (?, ?, ?, ?)
        ''', [
            (data['name'],
            data['rating'],
            data['age'],
            data['country'])
        ])
    conn.commit()
    await state.clear()


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.message.register(cmd_start, F.text == '/start')
    dp.message.register(name_chose, Form.name)
    dp.message.register(rating_chose, Form.rating)
    dp.message.register(age_chose, Form.age)
    dp.message.register(country_chose, Form.country)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
