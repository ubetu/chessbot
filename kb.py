import text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
class ConnectionCallback(CallbackData, prefix="conn"):
    id_asker: int
    asking: bool # True if it is ask, false if answer
    color = None
    game = None
    proved : bool

new_game_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text.new_game_button)]],
                                  resize_keyboard=True)

_button_yes = lambda message: InlineKeyboardButton(text="Да",
                                                   callback_data=ConnectionCallback(id_asker=message.from_user.id,
                                                                                    answer='Yes').pack())
_button_no = lambda message: InlineKeyboardButton(text="Нет",
                                                  callback_data=ConnectionCallback(id_asker=message.from_user.id,
                                                                                   answer='No').pack())
ask_to_join_kb = lambda message: InlineKeyboardMarkup(inline_keyboard=[[_button_yes(message), _button_no(message)]])

_accepeted_button = lambda color, game: InlineKeyboardButton(text=text.start_game,
                                                             callback_data=
                                                             ConnectionCallback(color=not color, game=game, asking=False).pack())
accepted_kb = lambda color, game: [[_accepeted_button(color, game)]]
#ask_to_join_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да")), ]])