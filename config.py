import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

config = {
    'APP_PORT': 9090,
    'APP_SESSION': os.getenv('APP_SESSION'),
    'PHONE': os.getenv('PHONE'),
    'API_KEY': os.getenv('API_KEY'),
    'API_HASH': os.getenv('API_HASH'),
    'CHANNELS': os.getenv('CHANNELS'),
    'MESSAGE': os.getenv('MESSAGE')
}