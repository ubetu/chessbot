from helpful.bot_creating import bot
from chess_api import GameManager
from aiogram.types import BufferedInputFile

async def send_board_photo(my_id: int, opponent_id: int, game: GameManager) -> None:
    """Отправляет картинку шахматного поля по user_id.
       Можно предавать state Любого из 2 игроков"""

    photo_bytes = game.create_image()
    photo_url = str(my_id) + '.png'

    photo = BufferedInputFile(photo_bytes, photo_url)
    await bot.send_photo(chat_id=my_id, photo=photo)
    await bot.send_photo(chat_id=opponent_id, photo=photo)
