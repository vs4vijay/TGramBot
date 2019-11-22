#!/usr/bin/env bash

# Pre-requisite: python3 -m pip install pyinstaller

echo "[+] Generating Binary"

CURRENT_DIR=$(pwd)

pyinstaller --onefile --clean --windowed \
            --add-data "${CURRENT_DIR}/telegram/gui/ui/form.ui:." \
            telegram/gui/telegram_gui.py 

# pyinstaller telegram_gui.spec
