#!/usr/bin/env python3

import asyncio
from gooey import Gooey, GooeyParser

from bot import Bot
from logger import logger
from config import config


name = 'Telegram Bot Command Center'

bot = None


def get_menus():
    menus = [{'name': 'Settings', 'items': [ { 'name': 'S1' }]},
             {'name': 'about', 'items': []}]
    return menus

@Gooey(program_name=name, 
        menus=get_menus(), 
        show_success_modal=False,
        show_restart_button=False, 
        return_to_config=True,
        navigation='SIDEBAR')
async def main(loop):

    print("--------------------------------------")
    print("    MOVIE SEARCH APP (GUI EDITION)")

    parser = GooeyParser()

    subparsers = parser.add_subparsers(help='commands', dest='action')

    # Session Initiate Input
    session_initiate_parser = subparsers.add_parser('Initiate_Session', help='HHHHHHHHHHH')
    session_initiate_parser.add_argument('session', metavar='Session Name', default='GUI', help='Enter the name of Session')
    session_initiate_parser.add_argument('api_key', metavar='API Key', type=int, default=config['API_KEY'], help='Enter API Key of Telegram')
    session_initiate_parser.add_argument('api_hash', metavar='API Hash', default=config['API_HASH'], help='Enter API Hash of Telegram')
    session_initiate_parser.add_argument('phone', metavar='Phone No.', default=config['PHONE'], help='Enter the phone number of the Account')

    # Session Start Input
    session_start_parser = subparsers.add_parser('Start_Session', help='')
    session_start_parser.add_argument('phone', metavar='Phone No.', default=config['PHONE'], help='Enter the phone number of the Account')
    session_start_parser.add_argument('code', metavar='Code', help='Enter the code which you received on Telegram')

    # Join Channels Input
    join_channel_parser = subparsers.add_parser('Join_Channel', help='')
    join_channel_parser.add_argument('channels', metavar='Channels', widget='BasicTextConsole', help='Enter the channels that you want join')
    # join_channel_parser.add_argument('code', metavar='Code', help='Enter the code which you received on Telegram')

    args = parser.parse_args()
    
    # session_start_parser.parse_args()

    print('args')
    print(args)

    asyncio.sleep(3)

    show_error_modal()



    # raise KeyError

    # test()

    # await session_initiate(loop, args)
    pass

def show_error_modal(error_msg = 'ok'):
    """ Spawns a modal with error_msg"""
    # wx imported locally so as not to interfere with Gooey
    import wx
    app = wx.App()
    dlg = wx.MessageDialog(None, error_msg, 'Error', wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()

def test():
    parser = GooeyParser()
    parser.add_argument('channels', metavar='Channels', widget='Textarea', help='Enter the channels that you want join')
    args = parser.parse_args()
    print('args')
    print(args)

async def session_initiate(loop, args):
    logger.info('Initiating a Telegram Session from API')
    global bot

    bot_config = {
        'APP_SESSION': args.session or config['APP_SESSION'],
        'PHONE': args.phone or config['PHONE'],
        'API_KEY': args.api_key or config['API_KEY'],
        'API_HASH': args.api_hash or config['API_HASH'],
        'APP_ENV': config['APP_ENV'],
        'TEST_SERVER': config['TEST_SERVER']
    }

    bot = Bot(bot_config)

    loop = asyncio.get_event_loop()
    data = await bot.initiate(loop)

    print(data)

    bot.client = data['client']

    response = {
        'success': True
    }
    if(data['started']):
        response['data'] = 'Session is started, you can start using the APIs'
    else:
        response['data'] = 'If you have received the code on telegram, use /sessions/start?code=<code> API to start the session'
    
    print(response)


async def session_start(args):
    phone = args.phone
    code = args.code

    await bot.sign_in(phone=phone, code=code)
        
    response = {
        'success': True, 
        'data': 'Session is started, you can start using the APIs'
    }
    print(response)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()