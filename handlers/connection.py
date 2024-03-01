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
        await bot.send_message(chat_id=message.text, text=text.ure_challenged.format(message.from_user.username),
                               reply_markup=kb.ask_to_join_kb(message, state))# предлогаем сыграть с нами
        await state.update_data(opponent_username=message.text)# запоминаем username оппонента
    except:
        await message.answer(text.incorrect_username) # обрабатываем неккоректный username, бот не может отправить сообщение,
        # передан не username

@router_connection.callback_query(ConnectionCallback.filter(F.ask))
async def answering_to_connect_try(callback:types.CallbackQuery, callback_data:ConnectionCallback, state:FSMContext):
    if callback_data.response == 'No':
        await bot.send_message(chat_id=callback_data.opponent_username, text=text.refused) #отказываем
        await callback_data.opponent_state.clear(callback.from_user.username) # очищаем state оппонента

    else:
        await state.set_state(GameFSM.playing)#меняем свое состояние

        color, color_me_str, color_opponent_str = chess_api.GameManager.random_color()
        game = chess_api.GameManager()
        my_username, opponent_username = callback.from_user.username, callback_data.opponent_username
        opponent_state = callback_data.opponent_state

        await callback.message.answer(text=text.your_color.format(color_me_str))
        await state.update_data(opponent_username=opponent_username, color=color, game=game,
                                opponent_state=opponent_state)

        await opponent_state.set_state(my_username, GameFSM.playing)
        await opponent_state.set_color(my_username, not color)
        await opponent_state.set_game(my_username, game)
        await opponent_state.set_opponent_state(my_username, state)

        await bot.send_message(chat_id=opponent_username, text=text.accepted.format(color_opponent_str))

        await send_board_photo(my_username, opponent_username, state)#
    # в date state'а: opponent_state, game, color, opponent_username
#@router_connection.callback_query(StateFilter(GameFSM.connecting), ConnectionCallback.filter(F.ask is False))
#async def start_game(callback:types.CallbackQuery,callback_data: ConnectionCallback, state:FSMContext):
    #await state.set_state(GameFSM.playing)
    #await state.update_data(game=callback_data.game, color=callback_data.color)

    #await send_board_photo(callback.from_user.id, state)
