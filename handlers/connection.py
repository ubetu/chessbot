import kb
import text
import chess_api

from bot_creating import bot
from state import GameFSM
from kb import ConnectionCallback
from support_functions import send_board_photo

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


router_connection = Router()

@router_connection.message(StateFilter(GameFSM.connecting))
async def asking_to_connect_try(message:Message, state:FSMContext):
    try:
        await bot.send_message(id=message.text, text=text.ure_challenged.format(id=message.from_user.id),
                               reply_markup=kb.ask_to_join_kb)
        await state.update_data(opponent_id=int(message.text))
    except:
        await message.answer(text.incorrect_id)

@router_connection.callback_query(ConnectionCallback.filter(F.ask))
async def answering_to_connect_try(callback:types.CallbackQuery, callback_data:ConnectionCallback, state:FSMContext):
    if callback_data.response == 'No':
        await bot.send_message(id=callback_data.id_asker, text=text.refused)
    else:
        await state.set_state(GameFSM.playing)
        color, color_me_str, color_opponent_str = chess_api.GameManager.random_color()
        game = chess_api.GameManager()
        await callback.message.answer(text=text.your_color.format(color_me_str))
        await state.update_data(opponent=callback_data.id_asker, color=color, game=game, move_count=0)
        await bot.send_message(id=callback_data.id_asker, text=text.accepted.format(color_opponent_str),
                               reply_markup=kb.accepted_kb(color,game))

        await send_board_photo(callback.from_user.id, state)#



@router_connection.callback_query(StateFilter(GameFSM.connecting), ConnectionCallback.filter(F.ask == False))
async def start_game(callback:types.CallbackQuery ,callback_data: ConnectionCallback, state:FSMContext):
    await state.set_state(GameFSM.playing)
    await state.update_data(game=callback_data.game, color=callback_data.color, move_count=0)


    await send_board_photo(callback.from_user.id, state)





    #игрок другой не начал игру, надо добавить