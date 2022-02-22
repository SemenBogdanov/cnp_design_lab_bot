import logging
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from create_bot import Dispatcher, bot, Projects
from aiogram import types
from help import msg

import keyboards
from my_handlers.api_google import rec_to_sheets, check_user
from my_handlers.chain_welcome import cmd_start


async def help_df(message: types.Message):
    await bot.send_message(message.chat.id, msg)


async def start_new_task(message: types.Message, state: FSMContext):
    u_name = check_user(str(message.from_user.id))
    # print(f'U_name is {u_name}')

    if len(u_name):
        await Projects.project_name.set()
        async with state.proxy() as data:
            data['user_from'] = u_name
        await bot.send_message(message.chat.id, '<b>Новая задача!</b>\n'
                                                f'Укажите название вашего проекта/инцидента (важно использовать '
                                                f'название как в Timesheets, например «Демография 2.0», '
                                                f'«Кураторство ПФО», если задача без проекта - укажите '
                                                f'«Презентации, макеты, сайты»).', parse_mode='HTML')
    else:
        await bot.send_message(message.chat.id, 'Вижу мы еще не знакомы, предлагаю это исправить!')
        await cmd_start(message)


async def get_chat_id(message: types.Message):
    await bot.send_message(message.chat.id, message.chat.id)


async def cancel_new_task(message: types.Message, state: FSMContext):
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
    await bot.send_message(message.chat.id, 'Cancelled.')


async def get_project_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['project_name'] = message.text
    await Projects.next()
    await bot.send_message(message.chat.id, "Укажите инициатора вашего проекта (например, Чернышенко Д.Н.) "
                           , parse_mode='HTML')


async def get_main_account(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['project_main_account'] = message.text
    await Projects.next()
    await bot.send_message(message.chat.id, "Для кого реализуем? (т.е кто является главным клиентом проекта/задачи, "
                                            "например, Мишустин М.В.)", parse_mode='HTML')


async def main_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['main_client'] = message.text
    await Projects.next()
    await bot.send_message(message.chat.id, "Опишите кратко задачу с указанием примерного объема и формата (например, "
                                            "подготовка презентации для сессии ПФО на 50 слайдов для широкого формата, "
                                            "создание макета для главной страницы дашборда)", parse_mode='HTML')


async def get_task_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['short_task_description'] = message.text
    await Projects.next()
    await bot.send_message(message.chat.id, "Установите дату и время"
                                            " сдачи в формате <b>'ДД.ММ.ГГГГ ЧЧ-ММ'</b>, например", parse_mode='HTML')


async def get_deadline_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['deadline_date'] = message.text
    await Projects.next()
    await bot.send_message(message.chat.id, "Как вы оцениваете важность проекта по шкале от 1 до 5 "
                                            "(где 1 - совсем неважно, 5 - крайне важно)", parse_mode='HTML',
                           reply_markup=keyboards.importance())


async def get_score_importance(query: types.CallbackQuery, callback_data, state: FSMContext):
    message = query.message
    await query.answer(f"Выбрано значение: {callback_data['imp']}")
    await query.message.delete_reply_markup()
    async with state.proxy() as data:
        data['score_importance'] = callback_data['imp']
    await Projects.next()

    # logging.info(data)
    # logging.info(message.message_id)
    await bot.send_message(message.chat.id, "Как вы оцениваете срочность проекта по шкале от 1 до 5 "
                                            "(где 1 - совсем несрочно, 5 - крайне срочно)", parse_mode='HTML',
                           reply_markup=keyboards.urgency())


async def callback_ret(query: types.CallbackQuery, callback_data, state: FSMContext):
    # logging.info(state)
    async with state.proxy() as data:
        data['score_urgency'] = callback_data['urgency']
        data['timestamp'] = str(datetime.now())
        data['task_status'] = 'New!'
    await query.answer(f"Выбрано значение {callback_data['urgency']}")
    await query.message.delete_reply_markup()

    message = query.message
    # logging.info(query)
    # logging.info(message.message_id)
    # await bot.edit_message_reply_markup(message.chat.id, message_id=int(message.message_id)-1)

    # await Projects.next()
    # async with state.proxy() as data:

    # # logging.info("Hello!")
    # logging.info(callback_data['val'])
    # logging.info(data['score_urgency'])
    await state.finish()
    ans = f"Внимание кухня! Новый заказ от {data['user_from']}:\n" \
          + "Проект: " + data['project_name'] + "\n" \
          + "Главный проекта: " + data['project_main_account'] + "\n" \
          + "Для кого реализуем: " + data['main_client'] + "\n" \
          + "Дедлайн (дата, время): " + data['deadline_date'] + "\n" \
          + "Описание: " + data['short_task_description'] + "\n" \
          + "Важность: " + data['score_importance'] + "\n" \
          + "Срочность: " + data['score_urgency'] + "\n" \
          + "Дата создания: " + data['timestamp'] + "\n" \
          + "Статус задачи: " + data['task_status'] + "\n"
    # logging.info(ans)
    # await bot.send_message(message.chat.id, ans) #for test
    await query.bot.send_message('-774044272', ans)

    try:
        # insert info into sheet
        if rec_to_sheets(data):
            await bot.send_message(message.chat.id, "Спасибо, ваш запрос отправлен в дизайн-лабораторию! "
                                                    "С вами скоро свяжутся)", parse_mode='HTML')

    except Exception as e:
        await bot.send_message(message.chat.id, "Произошел какой-то сбой. Данные, к сожалению, не записались :(")
        await bot.send_message('287994530', str(e) + '\nДанные для записи:\n' + str(data))


# register handlers
def register_chains(dp: Dispatcher):
    # Welcome
    dp.register_message_handler(start_new_task, commands=['new_task'])
    dp.register_message_handler(help_df, commands=['help'])
    dp.register_message_handler(get_chat_id, commands=['chat_id'])
    dp.register_message_handler(get_project_name, state=Projects.project_name)
    dp.register_message_handler(get_main_account, state=Projects.project_main_account)
    dp.register_message_handler(main_client, state=Projects.main_client)
    dp.register_message_handler(get_task_description, state=Projects.short_task_description)
    dp.register_message_handler(get_deadline_date, state=Projects.deadline)
    # dp.register_message_handler(get_deadline_time, state=Projects.deadline_time)
    # dp.register_message_handler(get_score_importance, state=Projects.score_importance)
    # dp.register_message_handler(get_score_urgency, state=Projects.score_urgency)
    dp.register_message_handler(get_chat_id, text=['чатид'])
    # Cancel
    dp.register_message_handler(cancel_new_task, state='*', commands='cancel')
    dp.register_message_handler(cancel_new_task, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_callback_query_handler(callback_ret, keyboards.call_urgency.filter(urgency=['1', '2', '3', '4', '5']),
                                       state='*')
    dp.register_callback_query_handler(get_score_importance,
                                       keyboards.call_importance.filter(imp=['1', '2', '3', '4', '5']),
                                       state=Projects.score_importance)
