import os
import sys
import asyncio

from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession, MemorySession
from telethon.tl.functions.messages import SendMessageRequest
from telethon.errors import FloodWaitError, MultiError, RPCError
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, InviteToChannelRequest

from telegram.core.logger import logger

SESSION_FOLDER = '.'

class Bot:

    def __init__(self, config):
        self.config = config

    async def initiate(self, loop=None):
        # self.session = MemorySession(config['APP_SESSION'])
        # self.session = MemorySession()
        session_file = f'{SESSION_FOLDER}/{self.config["APP_SESSION"]}'
        self.client = TelegramClient(session_file, self.config['API_KEY'], self.config['API_HASH'], loop=loop)
        self.client.session.save_entities = False
        session = StringSession.save(self.client.session)
        logger.info(f'SESSION Initiate: {session}')

        response = {
            'started': False,
            'session': session,
            'client': self.client
        }

        if(session is ''):
            if(self.config['APP_ENV'] == 'test'):
                logger.info('======== Connecting to Testing Server =========')
                self.client.session.set_dc(2, self.config['TEST_SERVER'], 80)
                await self.client.start(phone='9996629999', code_callback=lambda: '22222')
            else:
                if not self.client.is_connected():
                    logger.info('Client not connected, connecting now!')
                    await self.client.connect()
                
                if not await self.client.is_user_authorized():
                    logger.info('User not authorized, trying')
                    # await self.client.connect()
                    if(self.config.get('CODE') is not None):
                        await self.sign_in(phone=self.config['PHONE'], code=self.config.get('CODE'))
                    else:
                        await self.client.send_code_request(phone=self.config['PHONE'])
        else:
            print(f'------ initiate else {session}')
            await self.client.start(phone=self.config['PHONE'])
            response['started'] = True

        # client = self.client
        # @client.on(events.NewMessage)
        # async def echo_all(event):
        #     # logger.info(event)
        #     logger.info(f'[Received] {event.text}')
        #     # await event.reply(event.text)

        return response

    async def sign_in(self, phone, code):
        if not self.client.is_connected():
            logger.info('Client not connected, connecting now!')
            await self.client.connect()
        
        await self.client.sign_in(phone=phone, code=code)
        session = StringSession.save(self.client.session)
        logger.info(f'SESSION Sign in: {session}')

    async def me(self):
        me = await self.client.get_me()
        return me

    async def get_all_conversations(self):
        dialogs = await self.client.get_dialogs()
        return dialogs

    async def send_message(self, username, message):
        try:
            message = await self.client.send_message(username, message)
            return message
        except Exception as e:
            logger.error(f'({username}) {e}')
            return None

    async def send_bulk_message(self, usernames, message):
        try:
            # await self.client.send_message(usernames[0], message)
            # await asyncio.wait([
            #     self.client.send_message(username, message) for username in usernames
            # ])
            await self.client([
                SendMessageRequest(username, message) for username in usernames
            ], ordered=True)
        except FloodWaitError as e:
            logger.error(f'FloodWaitError: {e} {sys.exc_info()}')
            # TODO: Notify
            return { 'error': str(e) }
        except MultiError as e:
            logger.error(f'MultiError: {e} - {sys.exc_info()}')
            # Success results are stored in "e.results", errors are stored in "e.exceptions"

            output = {}
            for index in range(len(usernames)):
                username = usernames[index]
                result = e.results[index]
                if(result):
                    output[username] = { 'sent': True, 'result': result }
                else:
                    error = e.exceptions[index]
                    output[username] = { 'sent': False, 'error': str(error) }
            return output
        except Exception as e:
            logger.error(f'Exception: {e} - {sys.exc_info()}')

            output = {}
            for username in usernames:
                output[username] = { 'sent': False, 'error': str(e) }
            return output

    async def get_entity(self, name):
        try:
            entity = await self.client.get_entity(name)
            return { 'entity': entity }
        except Exception as e:
            logger.error(f'({name}) {e} {sys.exc_info()}')
            return { 'error': str(e) }

    async def get_channel(self, channel):
        try:
            ch = await self.client.get_entity(channel)
            return { 'channel': ch }
        except Exception as e:
            logger.error(f'({channel}) {e} {sys.exc_info()}')
            return { 'error': str(e) }
    
    async def join_channel(self, channel):
        ch = await self.get_channel(channel)
        print(f'ch: {channel}')
        print(ch)
        if(ch and ch.get('channel')):
            print('if')
            try:
                ch_joined = await self.client(JoinChannelRequest(ch['channel']))
                if(len(ch_joined.updates) is not 0):
                    logger.info(f'(Channel:{channel}) Joined')
                return { 'joined': True, 'channel': ch['channel'] }
            except Exception as e:
                logger.error(f'({channel}) {e} {sys.exc_info()}')
                return { 'error': str(e) }
        else:
            print('else')
            return { 'error': ch.get('error') }
    
    async def leave_channel(self, channel):
        ch = await self.get_channel(channel)
        ch_left = await self.client(LeaveChannelRequest(ch))
        return ch_left

    async def join_channels_and_send_message(self, channels, message):
        # Joining the channels
        [ await self.join_channel(channel) for channel in channels ]
        results = {}
        for channel in channels:
            ch = await self.join_channel(channel)
            if(ch.get('joined')):
                results[channel] = { 'joined': True }
            else:
                results[channel] = { 'error': ch.get('error') }
        
        joined_channels = filter(lambda channel: results[channel].get('joined') == True, channels)
        joined_channels = list(joined_channels)

        logger.info(f'Joined Channels: {joined_channels}')

        if(len(joined_channels) > 0):
            try:
                data = await self.send_bulk_message(joined_channels, message)
                for channel in joined_channels:
                    results[channel].update(data[channel])
            except Exception as e:
                logger.error(f'{e} - {sys.exc_info()}')
                data = e
        else:
            logger.info('No channels joined')
        return results

    async def invite_users(self, channels, users):
        results = {}

        for user in users:
            entity = await self.get_entity(user)
            if(entity.get('entity')):
                results[user] = { 
                    'type': 'user',
                    'valid': True
                }
            else:
                results[user] = { 
                    'type': 'user',
                    'error': entity.get('error')
                }

        valid_users = filter(lambda user: results[user].get('valid') == True, users)
        valid_users = list(valid_users)

        print('valid_users users')
        print(valid_users)

        # channels = [ channels[0] ] if channels else []

        for channel in channels:
            # Make sure channel is joined first
            ch = await self.join_channel(channel)
            if(ch.get('joined')):
                results[channel] = {
                    'type': 'channel',
                    'joined': True
                }
                try:
                    data = await self.client(InviteToChannelRequest(ch.get('channel'), valid_users))
                except Exception as e:
                    logger.error(f'{e} - {sys.exc_info()}')
                    data = e
                print('invite_users data: ')
                print(data)
            else:
                results[channel] = {
                    'type': 'channel',
                    'error': ch.get('error') 
                }
        return results