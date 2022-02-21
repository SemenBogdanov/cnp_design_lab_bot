from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

call_data1 = CallbackData('data1', 'num1')
call_data2 = CallbackData('wantAsk', 'wantAsk')
call_data3 = CallbackData('data2', 'num2')
call_urgency = CallbackData('data3', 'num3')


def rate_urgency():
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton('1', callback_data=call_urgency.new(num3='1')),
        InlineKeyboardButton('2', callback_data=call_urgency.new(num3='2')),
        InlineKeyboardButton('3', callback_data=call_urgency.new(num3='3')),
        InlineKeyboardButton('4', callback_data=call_urgency.new(num3='4')),
        InlineKeyboardButton('5', callback_data=call_urgency.new(num3='5')),
    )


def get_keyboard():
    return InlineKeyboardMarkup().row(
        KeyboardButton('Пора ли звонить?', callback_data=call_data1.new(num1='1')),
    ).row(
        KeyboardButton('Услуги и цены', callback_data=call_data1.new(num1='2')),
        KeyboardButton('Алгоритм работы', callback_data=call_data1.new(num1='3')),
    ).row(
        KeyboardButton('Команда', callback_data=call_data1.new(num1='4')),
        KeyboardButton('Контакты', callback_data=call_data1.new(num1='5')),
        KeyboardButton('Об авторе...', callback_data=call_data1.new(num1='6')),
    ).row(
        InlineKeyboardButton(text='Оставить заявку и получить бонус!', url='https://big-career.ru/',
                             callback_data=call_data1.new(num1='7')),
    )


def keyboard2():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton('---Задать вопрос!---')
    )


def keyboard3():
    return InlineKeyboardMarkup(resize_keyboard=True).row(
        InlineKeyboardButton(text='Я ПРОСТО УЗНАТЬ', callback_data=call_data3.new(num2='0'))
    ).row(
        InlineKeyboardButton(text='Я ХОЧУ РЕЗЮМЕ', callback_data=call_data3.new(num2='1'))
    ).row(
        InlineKeyboardButton(text='ИДУ НА СОБЕСЕДОВАНИЕ', callback_data=call_data3.new(num2='2'))
    ).row(
        InlineKeyboardButton(text='РАБОТА МЕЧТЫ', callback_data=call_data3.new(num2='3'))
    )
