#!/usr/bin/env bash

# Pre-requisite: python3 -m pip install pyinstaller

echo "[+] Generating"
# pyinstaller --onefile --windowed telegram/gui/telegram_gui.py

pyinstaller telegram_gui.spec