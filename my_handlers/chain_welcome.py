import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from create_bot import Dispatcher, bot, Form
from aiogram import types

from my_handlers.api_google import check_user, add_user_info


async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Подождите. Проверяю пользователя...')
    u_name = check_user(message.from_user.id)
    print(f'u_id is {message.from_user.id}')
    print(f'u_name is {u_name}')
    if len(u_name):
        await bot.send_message(message.chat.id, f'Добрый день, {u_name}!')
        await bot.send_message(message.chat.id, '/new_task - оставить заявку на разработку дизайна\n'
                                                '/help - описание работы чат-бота')
        return
    else:
        await Form.user_name.set()
        await bot.send_message(message.chat.id, 'Представьтесь, '
                                                'пожалуйста! Например, вы можете написать "Иван Иванов". А ещё важно '
                                                'не ставить '
                                                'лишние пробелы и вводить данные в порядке: "Имя Фамилия"')


async def cancel_handler(message: types.Message, state: FSMContext):
    """
     Allow user to cancel any action
     """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await bot.send_message(message.chat.id, 'Cancelled.', reply_markup=types.ReplyKeyboardRemove())


async def get_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tg_id'] = message.from_user.id
        data['user_name'] = message.text
        data['tg_username'] = message.from_user.username
    await Form.next()
    await bot.send_message(message.chat.id, "Какую должность Вы занимаете в текущий момент?")


async def get_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_position'] = message.text

    await state.finish()
    try:
        add_user_info(data)
        await bot.send_message(message.chat.id, f"{data['user_name']}, вот и познакомились! "
                                                f"Если хотите оставить заявку на проект/работу, "
                                                f"нажмите /new_task")
    except Exception as e:
        await bot.send_message(message.chat.id, e)
        await bot.send_message(message.chat.id, "Произошла ошибка, я не смог Вас запомнить. "
                                                "Я уже оповестил разработчика.")

    # await bot.send_message(message.chat.id, f"Вот что я запомнил:\n{data['user_position']}, \n {data['user_name']}")


# register handlers
def register_chains(dp: Dispatcher):
    # Welcome
    dp.register_message_handler(cmd_start, Text(equals='привет', ignore_case=True))
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(get_username, state=Form.user_name)
    dp.register_message_handler(get_position, state=Form.user_position)

    # Cancel
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
