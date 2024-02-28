import asyncio

import kb
import text
import chess_api
from bot_creating import bot
from support_functions import send_board_photo, IsOurMove
from chess_api import GameManager

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from state import GameFSM
from kb import ConnectionCallback

router_playing = Router()
router_playing.callback_query.filter(StateFilter(GameFSM.playing))
router_playing.message.filter(StateFilter(GameFSM.playing))

@router_playing.message()
async def move_reaction(message:Message, state:FSMContext):
    user_data = await state.get_data()
    game: GameManager = user_data['game']
    if game.is_our_turn(user_data['color']):
        result, winner = game.is_finished()
        if result:
            await message.answer(text='')# игра закончена
            await bot.send_message(id=user_data['opponent'], text='')
        else:
            if game.is_legal_move(message.text):
                game.do_move(message.text)
            else:
                #неккоректный ход
                pass
    else:
        await message.answer('не твой ход')


