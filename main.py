#!/usr/bin/env python3

import sys

from telegram.core.config import config
from telegram.gui.telegram_gui import main_gui
# from telegram.api.server import main_api

if __name__ == '__main__':
    # API Server
    # port = sys.argv[1] if len(sys.argv) > 1 else config['PORT']
    # main_api(port=port)

    # GUI App
    main_gui()