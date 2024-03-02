from helpful import kb, text
import chess_api
from database.db import db

from helpful.bot_creating import bot
from state import GameFSM, Protect_state
from helpful.kb import ConnectionCallback
from handlers.support_functions import send_board_photo

from aiogram import types, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


router_connection = Router()

@router_connection.message(StateFilter(GameFSM.connecting))
async def asking_to_connect_try(message:Message, state:FSMContext):
    try:
        opponent_id = db.get_id(message.text)
        await bot.send_message(chat_id=opponent_id, text=text.ure_challenged.format(message.from_user.username),
                               reply_markup=kb.ask_to_join_kb(message.from_user.id))

        await state.update_data(opponent_id=opponent_id)# запоминаем username оппонента
    except:
        await message.answer(text.incorrect_username) # обрабатываем неккоректный username, бот не может отправить сообщение,
        # передан не username

@router_connection.callback_query(ConnectionCallback.filter())
async def answering_to_connect_try(callback:types.CallbackQuery, callback_data:ConnectionCallback, state:FSMContext):
    my_id, opponent_id = callback.from_user.id, callback_data.opponent_id

    if callback_data.answer == 'No':
        await bot.send_message(chat_id=opponent_id, text=text.refused) #отказываем
        await Protect_state.clear(my_id, opponent_id)# очищаем state оппонента

    else:
        await state.set_state(GameFSM.playing)#меняем свое состояние

        color, color_me_str, color_opponent_str = chess_api.GameManager.random_color()
        game = chess_api.GameManager()

        await callback.message.answer(text=text.your_color.format(color_me_str))
        await state.update_data(color=color, game=game, opponent_id=opponent_id)

        await Protect_state.set_state(my_id, opponent_id, GameFSM.playing)
        await Protect_state.set_color(my_id, opponent_id, not color)
        await Protect_state.set_game(my_id, opponent_id, game)

        await bot.send_message(chat_id=opponent_id, text=text.accepted.format(color_opponent_str))

        await send_board_photo(my_id, opponent_id, game)#
    # в date state'а: opponent_state, game, color, opponent_username
