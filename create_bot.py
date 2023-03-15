import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from key import token

# from BotDB import BotDB


API_TOKEN = token

# Подключаем соответствующую конфигурацию логгирования документа
logging.basicConfig(level=logging.INFO)
#
# Создаем экземпляры классов Bot и Dispatcher, которые мы заранее ипортировали
# из библиотеки aiogram на строке 2
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    user_name = State()
    user_position = State()


class Projects(StatesGroup):
    project_name = State()
    # project_main_account = State()
    main_client = State()
    short_task_description = State()
    deadline = State()
    # deadline_time = State()
    # score_importance = State()
    # score_urgency = State()
    timestamp = State()



# try:
#     botDatabase = BotDB()
# except Exception as e:
#     print(e)
