#!/usr/bin/env python3

import sys
import signal
import asyncio

from bot import Bot
from config import config
from logger import logger

print(config)

bot = None

async def main(channels, message):
    bot = Bot(config)
    bot.client = await bot.start()

    me = await bot.me()
    logger.info(f'Me: {me.first_name} {me.last_name}: ID:{me.id}')

    conversations = await bot.get_all_conversations()
    # logger.info(f'Current Conversations: {conversations}')
    # logger.info([conversation.title for conversation in conversations])

    ch = await bot.join_channel('friendlyenga')
    # logger.info(ch.stringify())

    # message = await bot.send_message('volatality7', 'Hello, team!')
    # await bot.send_bulk_message(['volatality75', 'volatality7'], 'Hello, team!')


    # channels = config['CHANNELS']
    # message = config['MESSAGE']
    # if(channels and message):
    #     channels = channels.split(',')
    #     await bot.join_channels_and_send_message(channels, message)
    # else:
    #     logger.error('No channels or message are specified')
    #     sys.exit(1)


    await bot.client.run_until_disconnected()
    return None

def signal_handler(sig, frame):
        logger.info('Shutting down the bot')
        # await bot.client.disconnect()
        sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1], sys.argv[2]))
    loop.close()