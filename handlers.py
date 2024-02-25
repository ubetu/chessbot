import kb
import text

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command


router_main = Router()

@router_main.message(Command('/start'))
async def start(message: Message):
    await message.answer(text.greeting, reply_markup=kb.new_game_kb)

@router_main.message(F.text == text.new_game_button)
async def new_game(message: Message):
    await message.answer(text.new_game_started)