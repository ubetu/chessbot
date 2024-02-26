import text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



new_game_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text.new_game_button)]],
                                  resize_keyboard=True)

#ask_to_join_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да")), ]])