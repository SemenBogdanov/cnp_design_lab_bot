from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

call_urgency = CallbackData('urgency', 'urgency')
call_importance = CallbackData('imp', 'imp')


def urgency():
    keyboard = types.InlineKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(
        InlineKeyboardButton('1', callback_data=call_urgency.new(urgency='1')),
        InlineKeyboardButton('2', callback_data=call_urgency.new(urgency='2')),
        InlineKeyboardButton('3', callback_data=call_urgency.new(urgency='3')),
        InlineKeyboardButton('4', callback_data=call_urgency.new(urgency='4')),
        InlineKeyboardButton('5', callback_data=call_urgency.new(urgency='5')),
    )
    return keyboard


def importance():
    keyboard = types.InlineKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(
        InlineKeyboardButton('1', callback_data=call_importance.new(imp='1')),
        InlineKeyboardButton('2', callback_data=call_importance.new(imp='2')),
        InlineKeyboardButton('3', callback_data=call_importance.new(imp='3')),
        InlineKeyboardButton('4', callback_data=call_importance.new(imp='4')),
        InlineKeyboardButton('5', callback_data=call_importance.new(imp='5')),
    )
    return keyboard
