from aiogram.fsm.state import StatesGroup, State
class GameFSM(StatesGroup):
    connecting = State()
    playing = State()
    results_saying = State()