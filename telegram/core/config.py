import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# load_dotenv(find_dotenv())

config = {
    'APP_ENV': os.getenv('APP_ENV') or 'dev',
    'PORT': os.getenv('PORT'),
    'APP_SESSION': os.getenv('APP_SESSION'),
    'PHONE': os.getenv('PHONE'),
    'API_KEY': os.getenv('API_KEY'),
    'API_HASH': os.getenv('API_HASH'),
    'CHANNELS': os.getenv('CHANNELS'),
    'MESSAGE': os.getenv('MESSAGE'),
    'TEST_SERVER': os.getenv('TEST_SERVER')
}