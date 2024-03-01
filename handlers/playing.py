import kb
import text
from bot_creating import bot
from support_functions import send_board_photo
from chess_api import GameManager

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from state import GameFSM, transition_to_reconnecting

router_playing = Router()
router_playing.callback_query.filter(StateFilter(GameFSM.playing))
router_playing.message.filter(StateFilter(GameFSM.playing))

@router_playing.message()
async def move_reaction(message:Message, state:FSMContext):
    user_data = await state.get_data()
    game: GameManager = user_data['game']

    if game.is_our_turn(user_data['color']): # если наш ход
        if game.is_legal_move(move=message.text):
            game.do_move(message.text)

            await send_board_photo(message.from_user.username, user_data['opponent_username'], state)
            await bot.send_message(id=user_data['opponent_username'], message=message)# повторяем ход в чат противника

        else:
            await message.answer(text.incorrect_move)
    else:
        await message.answer(text.not_your_turn)

    result, winner = game.is_finished()
    if result != game.RES_PLAYING:  # кто-то выиграл
        result_text_we, result_text_opponent = (text.draw, text.draw) if result == game.RES_DRAW else\
            (text.ure_wined, text.ure_lost) if winner == user_data['color'] else (text.ure_lost, text.ure_lost)

        await state.clear()
        await user_data['opponent_state'].clear()
        #await transition_to_reconnecting(state)
        #await user_data['opponent_state'].transition_to_reconnecting(message.from_user.username,state)
        await message.answer(text=result_text_we)
        await bot.send_message(chat_id=user_data['opponent_username'], text=result_text_opponent)


