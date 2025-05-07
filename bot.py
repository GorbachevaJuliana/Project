import asyncio
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
API_TOKEN = ''
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
async def cmd_start(message,state):
    await state.clear()
    answers = ['Привет, как зовут игрока?', 'Введи имя игрока']
    await message.answer(random.choice(answers))
    await state.set_state(Form.name)

async def name_chose(message, state):
    await state.update_data(name=message.text)
    await message.answer('Введи рейтинг игрока')
    await state.set_state(Form.rating)

async def rating_chose(message, state):
    await state.update_data(rating=message.text)
    await message.answer('Сколько ему лет?')
    await state.set_state(Form.age)

async def age_chose(message, state):
    await state.update_data(age=message.text)
    await message.answer('Из какой он страны?')
    await state.set_state(Form.country)

async def country_chose(message, state):
    await state.update_date(country=message.text)
    


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.message.register(cmd_start, F.text == '/start')
    dp.message.register(gender_chose, Form.gender)
    dp.message.register(name_chose, Form.name)
    await dp.start_polling(bot)

asyncio.run(main())