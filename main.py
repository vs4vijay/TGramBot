#!/usr/bin/env python3

import sys

from server import app
from config import config

if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else config['PORT']
    app.run(host='0.0.0.0', port=port, auto_reload=True)