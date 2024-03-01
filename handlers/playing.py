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

    if game.is_our_turn(user_data['color']): # если наш ход
        result, winner = game.is_finished()
        if game.is_legal_move(move=message.text):
            game.do_move(message.text)

            await send_board_photo(message.from_user.id, state)#в наш чат
            await send_board_photo(user_data['opponent'], state)# в чат оппоннта
            await bot.send_message(id=user_data['opponent'], message=message)# повторяем ход в чат противника

        else:
            await message.answer(text.incorrect_move)
    else:
        await message.answer(text.not_your_turn)z

    result, winner = game.is_finished()
    if result == game.RES_WIN:  # кто-то выиграл
        result_text_we, result_text_opponent = (text.ure_wined, text.ure_lost) if winner == user_data['color'] \
            else (text.ure_lost, text.ure_lost)
        await message.answer(text=result_text_we + text.else_one_game, reply_markup=kb.ask_to_join_kb(message))
        await bot.send_message(id=user_data['opponent'], text=result_text_opponent + text.else_one_game)

    elif result == game.RES_DRAW:
        await message.answer(text=text.draw + text.else_one_game, reply_markup=kb.ask_to_join_kb(message))
        await bot.send_message(id=user_data['opponent'], text=result.text.draw + text.else_one_game)



      # ничья
        await message.answer(text=text.draw + text.else_one_game)
        await bot.send_message(id=user_data['opponent'], text=text.draw + text.else_one_game)


