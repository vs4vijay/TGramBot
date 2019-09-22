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
            '/me': 'Get Account info.',
            '/channels/join': 'Joins the list of channels',
            '/messages/send': 'Send message to list of channels',
            '/conversations': 'Get Conversations',
            '/feeds': 'Get realtime feeds'
        }
    }
    return json(data)

@telegram_bp.route('/sessions/initiate')
@doc.summary('Initiate a Session')
@doc.consumes(doc.String(name='session'), doc.String(name='phone'), 
              doc.String(name='api_key'), doc.String(name='api_hash'), location='query')
async def session_initiate(request):
    logger.info('Initiating a Telegram Session from API')
    global bot

    bot_config = {
        'APP_SESSION': request.args.get('session') or config['APP_SESSION'],
        'PHONE': request.args.get('phone') or config['PHONE'],
        'API_KEY': request.args.get('api_key') or config['API_KEY'],
        'API_HASH': request.args.get('api_hash') or config['API_HASH'],
        'APP_ENV': config['APP_ENV'],
        'TEST_SERVER': config['TEST_SERVER']
    }
    bot = Bot(bot_config)

    loop = asyncio.get_event_loop()
    bot.client = await bot.start(loop)

    return json({ 'success': True, 'data': 'If you have received the code on telegram, use /sessions/start?code=<code> API to start the session' })

@telegram_bp.route('/sessions/start')
@doc.summary('Start a session with code received on telegram app')
@doc.consumes(doc.String(name='code'), location='query')
async def session_start(request):
    code = request.args.get('code')

    if(code):
        logger.info(f'Starting a session with code: {code}')
        await bot.client.sign_in(code=code)
    else:
        return json({'success': False, 'error': 'code is required'}, status=400)
    
    return json({'success': True})

@telegram_bp.route('/me')
@doc.summary('Get Account info.')
@doc.produces({'success': doc.Boolean, 'data': {}})
async def send_messages(request):

    if(bot and await bot.client.is_user_authorized()):
        me = await bot.me()
    else:
        raise Exception('Session not started')

    logger.info(f'Me: {me.first_name} {me.last_name}: ID:{me.id}')

    data = {
        'success': True,
        'data': me.stringify()
    }
    return json(data)

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

    channels = channels.split(',')

    results = await bot.join_channels_and_send_message(channels, message)

    is_success = len(list(filter(lambda channel: results[channel].get('error') is not None, channels))) is 0

    data = {
        'success': is_success,
        'data': {
            'message': message,
            'channels': results
        }
    }
    return json(data)

@telegram_bp.route('/channels/join')
@doc.summary('Joins the list of channels')
@doc.consumes(doc.String(name='channels'), location='query')
@doc.produces({'success': doc.Boolean, 'data': {}})
async def send_messages(request):
    channels = request.args.get('channels')

    data = {
        'success': False,
        'error': ''
    }

    if(channels is None):
        data['error'] = 'No channels are specified'
        return json(data, status=400)

    channels = channels.split(',')

    # results = [await bot.join_channel(channel) for channel in channels]
    # results = map(lambda channel: { channel: await bot.join_channel(channel) }, channels)
    results = {}
    for channel in channels:
        results[channel] = await bot.join_channel(channel)

    data = {
        'success': True,
        'data': {
            'channels': results
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

@telegram_bp.route('/conversations')
@doc.summary('Get Conversations')
@doc.produces({'success': doc.Boolean, 'data': { 'conversations': [] }})
async def send_messages(request):

    if(bot and await bot.client.is_user_authorized()):
        conversations = await bot.get_all_conversations()
    else:
        raise Exception('Session not started')

    logger.info([conversation.title for conversation in conversations])

    data = {
        'success': True,
        'data': {
            'conversations': [conversation.title for conversation in conversations]
        }
    }
    return json(data)

@telegram_bp.route('/sessions/logout')
@doc.summary('Log out from a session')
async def session_logout(request):
    await bot.client.log_out()
    return json({'success': True})

@telegram_bp.listener('before_server_start')
async def before_server_start(app, loop):
    logger.info('Starting Telegram Client on Bootstrap')
    # loop = asyncio.get_event_loop()

    # global bot
    # bot = Bot(config)
    # bot.client = await bot.start(loop)

@telegram_bp.listener('after_server_stop')
async def after_server_stop(app, loop):
    logger.info('Stopping Telegram Client')
    if(bot):
        await bot.client.disconnect()