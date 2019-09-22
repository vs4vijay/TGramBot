import os
import sys
import asyncio

from telethon.errors import FloodWaitError
from telethon.sessions import StringSession, MemorySession
from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

from logger import logger

class Bot:

    def __init__(self, config):
        self.config = config

    async def start(self, loop=None):
        # self.session = MemorySession(config['APP_SESSION'])
        # self.session = MemorySession()
        self.client = TelegramClient(self.config['APP_SESSION'], self.config['API_KEY'], self.config['API_HASH'], loop=loop)
        # self.client.session.save_entities = False

        print("self.config['APP_ENV']", self.config['APP_ENV'])

        if(self.config['APP_ENV'] == 'test'):
            logger.info('======== Connecting to Testing Server =========')
            self.client.session.set_dc(2, self.config['TEST_SERVER'], 80)
            await self.client.start(phone=self.config['PHONE'] or '9996629999', code_callback=lambda: '22222')
        else:
            logger.info('else block')
            await self.client.start(phone=self.config['PHONE'])
            
        client = self.client

        @client.on(events.NewMessage)
        async def echo_all(event):
            # logger.info(event)
            logger.info(f'[Received] {event.text}')
            # await event.reply(event.text)

        return self.client

    async def me(self):
        me = await self.client.get_me()
        logger.info(f'[ME] {me}')
        return me

    async def get_all_conversations(self):
        dialogs = await self.client.get_dialogs()
        return dialogs

    async def send_message(self, username, message):
        try:
            message = await self.client.send_message(username, message)
            logger.info(message)
            return message
        except Exception as e:
            logger.error(f'({username}) {e}')
            return None

    async def send_bulk_message(self, usernames, message):
        try:
            await asyncio.wait([
                self.client.send_message(username, message) for username in usernames
            ])
        except FloodWaitError as e:
            logger.error(e)
            # TODO: Notify
        except Exception as e:
            logger.error(e)
            return None

    async def get_channel(self, channel):
        try:
            ch = await self.client.get_entity(channel)
            return { 'channel': ch }
        except Exception as e:
            logger.error(f'({channel}) {e} {sys.exc_info()}')
            return { 'error': str(e) }
    
    async def join_channel(self, channel):
        ch = await self.get_channel(channel)
        if(ch and ch.get('channel')):
            try:
                ch_joined = await self.client(JoinChannelRequest(ch['channel']))
                if(len(ch_joined.updates) is not 0):
                    logger.info(f'(Channel:{channel}) Joined')
                return { 'joined': ch_joined}
            except Exception as e:
                logger.error(f'({channel}) {e} {sys.exc_info()}')
                return { 'error': str(e) }
        else:
            return { 'error': ch.get('error') }
    
    async def leave_channel(self, channel):
        ch = await self.get_channel(channel)
        ch_left = await self.client(LeaveChannelRequest(ch))
        return ch_left

    async def join_channels_and_send_message(self, channels, message):
        # Joining the channels
        # [await self.join_channel(channel) for channel in channels]
        results = {}
        for channel in channels:
            ch = await self.join_channel(channel)
            if(ch.get('joined')):
                results[channel] = { 'joined': True }
            else:
                results[channel] = { 'error': ch.get('error') }
        
        joined_channels = filter(lambda channel: results['joined'] == True, channels)

        # Sending the messages
        data = await self.send_bulk_message(channels, message)
        print('--------- join_channels_and_send_message')
        print(data)
        return data
        