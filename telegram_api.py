import asyncio
import datetime as dt
from sanic import Blueprint
from sanic.response import json, stream
from sanic_openapi import doc

from bot import Bot
from config import config
from logger import logger


telegram_bp = Blueprint('telegram_api', url_prefix='/api/v1/telegram')

bot = None

@telegram_bp.route('/')
async def index(request):
    data = {
        'success': True, 
        'data': 'Telegram Bot APIs',
        'apis': {
            '/sessions/initiate': 'Initiate a Session',
            '/sessions/start': 'Start a session with code received on telegram app',
            '/sessions/logout': 'Log out from a session',
            '/messages/send': 'Send message to list of channels',
            '/feeds': 'Get realtime feeds'
        }
    }
    return json(data)

@telegram_bp.route('/sessions/initiate')
@doc.summary('Initiate a Session')
async def session_initiate(request):
    logger.info('Initiating a Telegram Session from API')
    loop = asyncio.get_event_loop()

    global bot
    bot = Bot(config, loop)

    try:
        bot.client = await bot.start(config)
    except Exception as e:
        logger.error(e)
        return json({'success': False, 'error': str(e)}, status=500)

    return json({'success': True})

@telegram_bp.route('/sessions/start')
@doc.summary('Start a session with code received on telegram app')
@doc.consumes(doc.String(name='code'), location='query')
async def session_start(request):
    code = request.args.get('code')

    if(code):
        logger.info(f'Starting a session with code: {code}')
        bot.client.sign_in(code=code)
    else:
        return json({'success': False, 'error': 'code is required'}, status=400)
    
    return json({'success': True})

@telegram_bp.route('/messages/send')
@doc.summary('Send message to list of channels')
@doc.consumes(doc.String(name='channels'), doc.String(name='message'), location='query')
@doc.produces({'success': doc.Boolean, 'data': {}})
async def send_messages(request):
    channels = request.args.get('channels')
    message = request.args.get('message')

    data = {
        'success': False,
        'error': ''
    }

    if(channels is None or message is None):
        data['error'] = 'No channels or message are specified'
        return json(data, status=400)

    me = await bot.me()
    logger.info(f'Me: {me.first_name} {me.last_name}: ID:{me.id}')

    channels = channels.split(',')
    channel = channels[0]
    ch = await bot.join_channel(channel)
    if(ch is None):
        data['error'] = f'Couldn\'t find or join channel {channel}'
        return json(data, status=400)

    # await bot.join_channels_and_send_message(channels, message)

    data = {
        'success': True,
        'data': {
            'channels': channels,
            'message': message
        }
    }
    return json(data)

async def get_data(stream, count=5):
    for i in range(count):
        await stream.write(f'{dt.datetime.now} </br>')
        # await asyncio.sleep(1)

@telegram_bp.route('/feeds')
@doc.summary('Get realtime feeds')
async def feeds(request):
    async def live_feeds(response):
        await response.write('foo</br>')
        await response.write('bar')
        # await get_data(response)
        for i in range(5):
            await response.write('viz </br>')
            await asyncio.sleep(1)

    return stream(live_feeds, content_type='text/html')

@telegram_bp.route('/sessions/logout')
@doc.summary('Log out from a session')
async def session_logout(request):
    await bot.client.log_out()
    return json({'success': True})

@telegram_bp.listener('before_server_start')
async def before_server_start(app, loop):
    logger.info('Starting Telegram Client')
    # loop = asyncio.get_event_loop()

    # global bot
    # bot = Bot(config, loop)
    # bot.client = await bot.start(config)

@telegram_bp.listener('after_server_stop')
async def after_server_stop(app, loop):
    logger.info('Stopping Telegram Client')
    await bot.client.disconnect()