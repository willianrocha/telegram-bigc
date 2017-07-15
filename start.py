from bc import BigC
import time
import logging
import os

import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
import asyncio


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    token = os.environ.get('TELEGRAM_TOKEN')

    # bot = telepot.Bot(token)
    bot = telepot.aio.DelegatorBot(token, [
        pave_event_space()(
            per_chat_id(), create_open, BigC, timeout=10),
            ]
        )
    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot).run_forever())
    loop.run_forever()
