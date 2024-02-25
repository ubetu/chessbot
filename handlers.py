import kb
import text
import chess_api

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class GameFSM(StatesGroup):
    process = State()

router_main = Router()

@router_main.message(Command('/start'))
async def start(message: Message):
    await message.answer(text.greeting, reply_markup=kb.new_game_kb)

@router_main.message(F.text == text.new_game_button)
async def new_game(message: Message, state: FSMContext):
    await message.answer(text.new_game_started)
    await state.set_state(GameFSM.process)
    game = chess_api.GameManager()
    await state.update_data(game=game)
    await message.answer(text.greeting + game.color_text)
