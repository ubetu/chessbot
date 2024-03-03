from bot_creating import dp, bot

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

class GameFSM(StatesGroup):
    connecting = State()
    playing = State()
    reconnecting = State()

class Protect_state:

    @staticmethod
    def __get_opponent_state(opponent_id: int) -> FSMContext:
        opponent_storage_key = StorageKey(bot.id, opponent_id, opponent_id)
        return FSMContext(storage=dp.storage, key=opponent_storage_key)

    @classmethod
    def __rights_checking(cls, my_id: int, opponent_data) -> bool:
        if 'opponent_id' in opponent_data:
            return opponent_data['opponent_id'] == my_id
        return False

    @classmethod
    async def clear(cls, my_id: int, opponent_id:int) -> None:
        opponent_state = cls.__get_opponent_state(opponent_id)
        opponent_data = await opponent_state.get_data()
        if cls.__rights_checking(my_id, opponent_data):
            await opponent_state.clear()

    @classmethod
    async def set_state(cls, my_id: int, opponent_id:int, state: State) -> None:
        opponent_state = cls.__get_opponent_state(opponent_id)
        opponent_data = await opponent_state.get_data()
        if cls.__rights_checking(my_id, opponent_data):
            await opponent_state.set_state(state)

    @classmethod
    async def set_color(cls,my_id: int, opponent_id:int, color) -> None:
        opponent_state = cls.__get_opponent_state(opponent_id)
        opponent_data = await opponent_state.get_data()
        if cls.__rights_checking(my_id, opponent_data):
            await opponent_state.update_data(color=color)

    @classmethod
    async def set_game(cls,my_id: int, opponent_id:int, game) -> None:
        opponent_state = cls.__get_opponent_state(opponent_id)
        opponent_data = await opponent_state.get_data()
        if cls.__rights_checking(my_id, opponent_data):
            await opponent_state.update_data(game=game)
