import kb
import text
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from state import GameFSM

router_main = Router()
@router_main.message(Command('/start'))
async def start(message: Message):
    await message.answer(text.start.format(message.from_user.username), reply_markup=kb.new_game_kb)

@router_main.message(F.text == text.new_game_button)
async def new_game(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text.new_game_started)
    await state.set_state(GameFSM.connecting)
    await message.answer(text.enter_opponent_username)
