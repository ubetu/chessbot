import text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

new_game_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text.new_game_button)]],
                                  resize_keyboard=True)
