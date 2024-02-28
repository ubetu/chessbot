import os

from bot_creating import bot
from aiogram.fsm.context import FSMContext
from chess_api import GameManager
from aiogram.filters import BaseFilter

class IsOurMove(BaseFilter):
    def __init__(self, state: FSMContext):
        self.user_data = await state.get_data()

    def __call__(self):
        game: GameManager = self.user_data['game']
        our_color = self.user_data['color']
        if game.is_our_turn(our_color):
            return {'game': game}
        return False


async def send_board_photo(user_id: int, state: FSMContext) -> None:
    user_data = await state.get_data()
    photo_bytes = user_data['game'].create_image()
    photo_url = str(user_id) + '.png'

    with open(photo_url, 'wb') as photo:
        photo.write(photo_bytes)

    await bot.send_photo(photo_url)
    os.remove(photo_url)
