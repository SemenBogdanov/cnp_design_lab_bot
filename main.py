import asyncio
import logging
import my_handlers

from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    logging.info("Bot was started")


# register handlers from my_handlers_pocket
my_handlers.chain_welcome.register_chains(dp)
my_handlers.chain_task.register_chains(dp)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        # delay = 60 ** 2 * 12
        # loop.create_task(my_functions.other_functions.remind_me(delay))
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

    except Exception as error:
        print('except \n' + str(error))
        # botDatabase.conn.close()
