from asyncio import sleep
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class GameFSM(StatesGroup):
    connecting = State()
    playing = State()
    reconnecting = State()

async def transition_to_reconnecting(state: FSMContext) -> None:
    await state.set_state(GameFSM.reconnecting)
    opponent_id = (await state.get_data())['opponent_id']
    await state.set_data({'opponent_id': opponent_id})
    await sleep(30)# добавить в connection для проверки согласия
    user_data = await state.get_data()
    if len(user_data.values()) == 1:
        await state.clear()

class secure_state:
    def __init__(self, opponent_state: FSMContext) -> None:
        self.__opponent_state = opponent_state

    async def __rights_checking(self, username: str) -> bool:
        opponent_data = await self.__opponent_state.get_data()
        try:
            return opponent_data['opponent_username'] == username
        except:
            return False

    async def clear(self, username: str) -> None:
        if self.__rights_checking(username):
            await self.__opponent_state.clear()

    async def set_state(self, username: str, state:State) -> None:
        if self.__rights_checking(username):
            await self.__opponent_state.set_state(state)

    async def set_color(self, username: str, color) -> None:
        if self.__rights_checking(username):
            await self.__opponent_state.update_data(color=color)

    async def set_game(self, username: str, game) -> None:
        if self.__rights_checking(username):
            await self.__opponent_state.update_data(game=game)

    async def set_opponent_state(self, username: str, opponent_state: FSMContext) -> None:
        if self.__rights_checking(username):
            await self.__opponent_state.update_data(opponent_state=secure_state(opponent_state))

    async def transition_to_reconnecting(self, username: str) -> None:
        if self.__rights_checking(username):
            await transition_to_reconnecting(self.__opponent_state)
