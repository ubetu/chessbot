import text
from state import secure_state

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

class ConnectionCallback(CallbackData, prefix="conn"):
    opponent_username: str
    asking: bool # True if it is ask, false if answer
    opponent_state: secure_state
    #color = None
    #game = None
    #answer = None
    #proved: bool

new_game_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text.new_game_button)]],
                                  resize_keyboard=True)
def _button_yes(message, state):
    return InlineKeyboardButton(text="Да",
                                callback_data=ConnectionCallback(username_opponent=message.from_user.id,
                                                                 opponent_state=secure_state(state), answer='Yes', asking=True).pack())
def _button_no(message, state):
    return InlineKeyboardButton(text="Нет",
                                callback_data=ConnectionCallback(username_opponent=message.from_user.id,
                                                                 answer='No', opponent_state=secure_state(state), asking=True).pack())
def ask_to_join_kb(message, state):
    return InlineKeyboardMarkup(inline_keyboard=[[_button_yes(message, state), _button_no(message, state)]])

def _accepeted_button(color, game):
    return InlineKeyboardButton(text=text.start_game,
                                callback_data=ConnectionCallback(color=not color, game=game, asking=False).pack())
def accepted_kb (color, game):
    return [[_accepeted_button(color, game)]]
