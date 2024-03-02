from database.db import db
from helpful import text
from helpful.bot_creating import bot
from handlers.support_functions import send_board_photo
from chess_api import GameManager

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from state import GameFSM, Protect_state

router_playing = Router()
router_playing.message.filter(StateFilter(GameFSM.playing))

@router_playing.message()
async def move_reaction(message:Message, state:FSMContext):
    user_data = await state.get_data()
    game: GameManager = user_data['game']
    my_id, opponent_id = message.from_user.id, user_data['opponent_id']

    if game.is_our_turn(user_data['color']): # если наш ход
        if game.is_legal_move(move=message.text):
            game.do_move(message.text)

            await send_board_photo(my_id, opponent_id, game)
            await bot.send_message(chat_id=opponent_id, text=message)# повторяем ход в чат противника

        else:
            await message.answer(text.incorrect_move)
    else:
        await message.answer(text.not_your_turn)

    result, winner = game.is_finished()
    if result != game.RES_PLAYING:  # кто-то выиграл
        #определяем текст для нас и оппонента взависимости от результата
        result_text_we, result_text_opponent = (text.draw, text.draw) if result == game.RES_DRAW else\
            (text.ure_wined, text.ure_lost) if winner is user_data['color'] else (text.ure_lost, text.ure_lost)

        # определяем id белых и черных
        white_id, black_id = (my_id, opponent_id) if user_data['color'] is game.WHITE \
            else (opponent_id, my_id)

        # определяем результат в -1/0/1 нотации
        result_int = 1 if winner is game.WHITE else -1 if winner is game.BLACK else 0
        db.write_game_results(white_id, black_id, result_int)

        #очищаем наш state и state оппонента
        await state.clear()
        await Protect_state.clear(message.from_user.id, user_data['id'])

        await message.answer(text=result_text_we)
        await bot.send_message(chat_id=opponent_id, text=result_text_opponent)
