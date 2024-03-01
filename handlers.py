import kb
import text
import chess_api
from bot_creating import bot
import asyncio
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from state import GameFSM
from kb import ConnectionCallback




@router_main.message(StateFilter(GameFSM.connecting))
async def connecting(message:Message, state:FSMContext):
    try:
        await bot.send_message(id=message.text, text=text.ure_challenged.format(id=message.from_user.id), reply_markup=kb.ask_to_join_kb)
        await state.update_data(opponent_id=int(message.text), answered=False)
    except:
        await message.answer(text.incorrect_id)

@router_main.callback_query(ConnectionCallback.filter())
async def responcing_to_connect_try(callback:types.CallbackQuery, callback_data:ConnectionCallback, state:FSMContext):
    if callback_data.response == 'No':
        try:
            await bot.send_message(id=callback_data.id_opponent, text='Тебе отказали')
        except:
            pass
    else:
        await state.set_state(GameFSM.playing)
        color, color_str = chess_api.GameManager.random_color()
        game = chess_api.GameManager()
        await state.update_data(opponent=callback_data.id_opponent, color=color, game=game)
        await bot.send_message(id=callback_data.id_opponent, text='Согласился! Чтобы начать играть нажмите Начать игру',
                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Начать игру',
                                                                callback_data=ConnectionCallback(color=not color, game=game))]]))
