import text

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

class ConnectionCallback(CallbackData, prefix="conn"):
    opponent_id: int
    answer: str

new_game_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text.new_game_button)]],
                                  resize_keyboard=True)
def _button_yes(opponent_id:int):
    return InlineKeyboardButton(text="Да",
                                callback_data=ConnectionCallback(opponent_id=opponent_id, answer='Yes').pack())
def _button_no(opponent_id:int):
    return InlineKeyboardButton(text="Нет",
                                callback_data=ConnectionCallback(opponent_id=opponent_id, answer='No').pack())
def ask_to_join_kb(opponent_id:id):
    return InlineKeyboardMarkup(inline_keyboard=[[_button_yes(opponent_id),
                                                  _button_no(opponent_id)]])
