import asyncio
import os
import random
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
# from dotenv import load_dotenv
API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
conn = sqlite3.connect('project_db.db')
cursor = conn.cursor()

class Form(StatesGroup):
    name = State()
    rating = State()
    age = State()
    country = State()
    photo = State()
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
    await state.update_data(type=callback)
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
    await message.answer("Теперь отправьте фото игрока:")
    await state.set_state(Form.photo)


async def photo_chose(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    photo_data = await bot.download_file(file.file_path)
    photo_bytes = photo_data.read()
    data = await state.get_data()
    cursor.executemany('''
        INSERT INTO player (name, rating, age, country, photo)
        VALUES (?, ?, ?, ?, ?)
        ''', [
            (data['name'],
            data['rating'],
            data['age'],
            data['country'],
            photo_bytes)
        ])
    
    conn.commit()
    await message.answer(f"Твои данные {data}")
    await state.clear()

@dp.message(F.text == "/list")
async def list_dogs(message: Message):
    cursor.execute("SELECT name, country FROM player")
    rows = cursor.fetchall()

    if not rows:
        await message.answer("В базе пока нет ни одного игрока.")
        return

    for name, country in rows:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Фото", callback_data=f"photo:{name}")]
        ])
        await message.answer(f"{name} - {country}", reply_markup=keyboard)


# Обработка кнопок для отправки фотографии у каждого игрока
@dp.callback_query(F.data.startswith("photo:"))
async def send_dog_photo(callback):
    player_name = callback.data.split(":")[1]

    cursor.execute("SELECT name, country, photo FROM player WHERE name = ?", (player_name,))
    row = cursor.fetchall()[0]
    print(row)

    if row:
        name, country, photo_blob = row
        with open("temp.jpg", "wb") as f:
            f.write(photo_blob)

        photo = FSInputFile("temp.jpg")
        await callback.message.answer_photo(photo, caption=f"{name}\n Страна: {country}")
        os.remove("temp.jpg")
    else:
        await callback.message.answer(" не найдено.")

    await callback.answer()
