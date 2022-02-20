import logging
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import Dispatcher, bot, Projects
from aiogram import types

from keyboards import rate_urgency
from my_handlers.api_google import rec_to_sheets, check_user
from my_handlers.chain_welcome import cmd_start


async def start_new_task(message: types.Message, state: FSMContext):
    u_name = check_user(str(message.from_user.id))
    # print(f'U_name is {u_name}')

    if len(u_name):
        await Projects.project_name.set()
        async with state.proxy() as data:
            data['user_from'] = u_name
        await message.reply('<b>Новая задача!</b>\n'
                            f'{u_name}, укажите название вашего проекта/инцидента (важно использовать название '
                            'как в Timesheet, например, "Водород" или "Кураторство ПФО") в свободной форме.',
                            parse_mode='HTML')
    else:
        await message.reply('Вижу мы еще не знакомы, предлагаю это исправить!')
        await cmd_start(message)


async def get_chat_id(message: types.Message):
    await message.reply(message.chat.id)


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
    await message.reply('Cancelled.')


async def get_project_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['project_name'] = message.text
    await Projects.next()
    await message.reply("Укажите инициатора вашего проекта (например, Чернышенко Д.Н.) <b>в свободной форме</b>",
                        parse_mode='HTML')


async def get_main_account(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['project_main_account'] = message.text
    await Projects.next()
    await message.reply("Опишите кратко задачу (например, подготовка презентации для "
                        "сессии ПФО для широкого экрана) <b>в свободной форме</b>", parse_mode='HTML')


async def get_task_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['short_task_description'] = message.text
    await Projects.next()
    await message.reply("Установите срок сдачи в формате <b>'ДД.ММ.ГГГГ'</b>", parse_mode='HTML')


async def get_deadline_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['deadline_date'] = message.text
    await Projects.next()
    await message.reply("Установите срок сдачи по времени в формате <b>'ЧЧ-ММ'</b>", parse_mode='HTML')


async def get_deadline_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['deadline_time'] = message.text
    await Projects.next()
    await message.reply("Как вы оцениваете важность проекта по шкале от 1 до 5 "
                        "(где 1 - совсем неважно, 5 - крайне важно)", parse_mode='HTML')


async def get_score_importance(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['score_importance'] = message.text
    await Projects.next()
    await message.reply("Как вы оцениваете срочность проекта по шкале от 1 до 5 "
                        "(где 1 - совсем несрочно, 5 - крайне срочно)", parse_mode='HTML')


async def get_score_urgency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['score_urgency'] = message.text
        data['timestamp'] = str(datetime.now())
        data['task_status'] = 'New!'
    await state.finish()

    ans = f"Внимание кухня! Новый заказ от {data['user_from']}:\n" \
          + "Проект: " + data['project_name'] + "\n" \
          + "Главный проекта: " + data['project_main_account'] + "\n" \
          + "Дедлайн (дата): " + data['deadline_date'] + "\n" \
          + "Дедлайн (время): " + data['deadline_time'] + "\n" \
          + "Описание: " + data['short_task_description'] + "\n" \
          + "Важность: " + data['score_importance'] + "\n" \
          + "Срочность: " + data['score_urgency'] + "\n" \
          + "Дата создания: " + data['timestamp'] + "\n" \
          + "Статус задачи" + data['task_status'] + "\n"
    await message.bot.send_message('-774044272', ans)

    try:
        # insert info into sheet
        if rec_to_sheets(data):
            await message.reply("Спасибо, ваш запрос отправлен в дизайн-лабораторию! С вами скоро свяжутся)",
                                parse_mode='HTML')

    except Exception as e:
        await message.reply("Произошел какой-то сбой. Данные, к сожалению, не записались :(")
        await bot.send_message('287994530', str(e) + '\nДанные для записи:\n' + str(data))


# register handlers
def register_chains(dp: Dispatcher):
    # Welcome
    dp.register_message_handler(start_new_task, commands=['new_task'])
    dp.register_message_handler(get_chat_id, commands=['chat_id'])
    dp.register_message_handler(get_project_name, state=Projects.project_name)
    dp.register_message_handler(get_main_account, state=Projects.project_main_account)
    dp.register_message_handler(get_task_description, state=Projects.short_task_description)
    dp.register_message_handler(get_deadline_date, state=Projects.deadline)
    dp.register_message_handler(get_deadline_time, state=Projects.deadline_time)
    dp.register_message_handler(get_score_importance, state=Projects.score_importance)
    dp.register_message_handler(get_score_urgency, state=Projects.score_urgency)
    dp.register_message_handler(get_chat_id, text=['чатид'])
    # Cancel
    dp.register_message_handler(cancel_new_task, state='*', commands='cancel')
    dp.register_message_handler(cancel_new_task, Text(equals='cancel', ignore_case=True), state='*')
