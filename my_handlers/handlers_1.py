from aiogram.dispatcher.filters.state import StatesGroup, State

from create_bot import Dispatcher
from aiogram import types




# async def reply_welcome(message: types.Message):
#     await message.reply('Здравствуйте! Я помогу составить запрос в дизайн-лабораторию КЦ. Представьтесь, пожалуйста! '
#                         'Например, вы можете написать "Иван Иванов". А ещё важно не ставить лишние пробелы и вводить '
#                         'данные в порядке: "Имя Фамилия"')


# # register handlers
# def register_handlers_1(dp: Dispatcher):
#     dp.register_message_handler(reply_welcome, text=['Привет!'])

#     dp.register_message_handler(reply_welcome, text=welcome_keywords)
