#!/usr/bin/env python3

import sys

from sanic import Sanic
from sanic.response import json
from sanic.exceptions import NotFound, SanicException
from sanic_openapi import swagger_blueprint

from telegram.core.config import config
from telegram.core.logger import logger
from telegram.api.telegram_api import telegram_bp


app = Sanic()

# Adding Blueprint for Telegram Bot
app.blueprint(telegram_bp)

# Adding OpenAPI Specs with custom url prefix
swagger_blueprint.url_prefix = '/api/docs'
app.blueprint(swagger_blueprint)
app.config['API_BASEPATH'] = '/'
app.config['API_SCHEMES'] = ['http', 'https']
app.config['API_VERSION'] = '1.0.0'
app.config['API_TITLE'] = 'TGramBot'
app.config['API_DESCRIPTION'] = 'OpenAPI Specs for Telegram Bot'
# app.config['API_SECURITY'] = [{'BasicAuth': []}]
# app.config['API_SECURITY_DEFINITIONS'] = {'BasicAuth': {'type': 'basic'}}
app.config['API_SECURITY_DEFINITIONS'] = { 'ApiKeyAuth': {'type': 'apiKey', 'in': 'header', 'name': 'api_key'} }


@app.route('/')
async def index(request):
    return json({'success': True, 'data': f'API docs are at {swagger_blueprint.url_prefix}'})

@app.exception(NotFound)
async def not_found_handler(request, exception):
    return json({'success': False, 'error': str(exception)}, status=404)

@app.exception(SanicException)
@app.exception(Exception)
async def exception_handler(request, exception):
    logger.error(f'Exception: {exception} - {sys.exc_info()}')
    return json({'success': False, 'error': str(exception)}, status=500)

def main_api(port = config['PORT']):
    # TODO: access_log=False, debug=False in production
    app.run(host='0.0.0.0', port=port, auto_reload=True)

if __name__ == '__main__':
    main_api()