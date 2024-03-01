from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class GameFSM(StatesGroup):
    connecting = State()
    playing = State()

class secur_state:
    def __init__(self, opponent_state: FSMContext) -> None:
        self.__opponent_state = opponent_state

    async def __rights_checking(self, my_id) -> bool:
        opponent_data = await self.__opponent_state.get_data()
        try:
            return opponent_data['opponent_id'] == my_id
        except:
            return False

    async

