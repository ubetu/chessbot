import kb
import text
import chess_api
from bot_creating import bot

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class GameFSM(StatesGroup):
    connecting = State()
    playing = State()
    results_saying = State()

class ConnectionCallback(CallbackData, prefix="conn"):
    id_asker: int
    #id_asked: int
    response: str
    color = None
    game = None

router_main = Router()

@router_main.message(Command('/start'))
async def start(message: Message):
    await message.answer(f"""Привет! Это бот для игры в шахматы и практики шахматной нотации. Твой ID: {message.from_user.id}
               Для начала игры нажми Новая игра""", reply_markup=kb.new_game_kb)

@router_main.message(StateFilter(None),F.text == text.new_game_button)
async def new_game(message: Message, state: FSMContext):
    await message.answer(text.new_game_started)
    await state.set_state(GameFSM.connecting)
    await message.answer('Введите ID человека, с которым в вы хотите сыграть')

@router_main.message(StateFilter(GameFSM.connecting))
async def connecting(message:Message, state:FSMContext):
    try:
        button_yes = InlineKeyboardButton(text="Да", callback_data=ConnectionCallback(id_asker=message.from_user.id,
                                                                                      answer='Yes'))
        button_no = InlineKeyboardButton(text="Нет", callback_data=ConnectionCallback(id_asker=message.from_user.id,
                                                                                      answer='No'))
        ask_to_join_kb = InlineKeyboardMarkup(inline_keyboard=[[button_yes, button_no]])
        await bot.send_message(id=message.text, text=f"С вами хочет играть {message.from_user.id}", reply_markup=ask_to_join_kb)
        await state.update_data(opponent_id=int(message.text))
    except:
        await message.answer("Некорректный ID. Пожалуйста, введите ID еще раз")

@router_main.callback_query(ConnectionCallback.filter())
async def responcing_to_connect_try(callback:types.CallbackQuery, callback_data:ConnectionCallback, state:FSMContext):
    if callback_data.response == 'No':
        try:
            await bot.send_message(id=callback_data.id_asker, text='Тебе отказали')
        except:
            pass
    else:
        await state.set_state(GameFSM.playing)
        color, color_str = chess_api.GameManager.random_color()
        game = chess_api.GameManager()
        await state.update_data(opponent=callback_data.id_asker, color=color, game=game)
        await bot.send_message(id=callback_data.id_asker, text='Согласился! Чтобы начать играть нажмите Начать игру',
                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Начать игру',
                                                                callback_data=ConnectionCallback(color=not color, game=game))]]))
