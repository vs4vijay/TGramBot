import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

config = {
    'APP_ENV': os.getenv('APP_ENV') or 'dev',
    'APP_PORT': os.getenv('APP_PORT') or 9090,
    'APP_SESSION': os.getenv('APP_SESSION'),
    'PHONE': os.getenv('PHONE'),
    'API_KEY': os.getenv('API_KEY'),
    'API_HASH': os.getenv('API_HASH'),
    'CHANNELS': os.getenv('CHANNELS'),
    'MESSAGE': os.getenv('MESSAGE')
}