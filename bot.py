import asyncio
import os
import random
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
API_TOKEN = '8003685426:AAGbaa-jzCyNoHPCLA-kZE8Ilq3WrVPyb5o'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
conn = sqlite3.connect('project_db.db')
cursor = conn.cursor()

class Form(StatesGroup):
    name = State()
    rating = State()
    age = State()
    country = State()
class TournamentForm(StatesGroup):
    name = State()
    date = State()
    place = State()
    players = State()
    type = State()
    games = State()

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

@dp.message(F.text == "/tournament")
async def find_command_handler(message:Message, state):
    await message.answer("Введи название турнира")
    await state.set_state(TournamentForm.date)

async def date_chose(message:Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Введи дату начала турнира")
    await state.set_state(TournamentForm.place)

async def place_chose(message:Message, state: FSMContext):
    await state.update_data(place=message.text)
    await message.answer('Введи место где будет турнир')
    await state.set_state(TournamentForm.players)

async def players_chose(message:Message, state: FSMContext):
    await state.update_data(players=message.text)
    await message.answer('Введи всех игроков')
    await state.set_state(TournamentForm.type)
    
    
@dp.callback_query(lambda c: c.data in ['ATP 1000', 'WTA 1000', 'ATP 500', 'WTA 500', 'Challenger', 'Wimbledon', 'Roland Garros', 'Australian Open', 'US Open',])
async def handle_yes(callback, state):
    print(callback)
    await state.update_data(type)
    await callback.answer()
    await callback.message.answer('Напиши все матчи')
    await state.set_state(Form.games)

async def games_chose(message:Message, state: FSMContext):
    await state.update_data(games=message.text)
    data = await state.get_data()
    await message.answer(f"Твои данные {data}")
    cursor.executemany('''
        INSERT INTO tournament (name, date, place, players, type)
        VALUES (?, ?, ?, ?, ?)
        ''', [
            (data['name'],
            data['date'],
            data['place'],
            data['players'],
            data['type'])
        ])
    conn.commit()
    await state.clear()

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
    dp.message.register(cmd_start, F.text == '/start')
    dp.message.register(cmd_start, F.text == '/tournament')
    dp.message.register(name_chose, Form.name)
    dp.message.register(rating_chose, Form.rating)
    dp.message.register(age_chose, Form.age)
    dp.message.register(country_chose, Form.country)
    dp.message.register(find_command_handler, TournamentForm.name)
    dp.message.register(date_chose, TournamentForm.date)
    dp.message.register(place_chose, TournamentForm.place)
    dp.message.register(players_chose, TournamentForm.players)
    dp.message.register(handle_yes, TournamentForm.type)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
