ECHO OFF

# Pre-requisite: python3 -m pip install pyinstaller

ECHO "[+] Generating Binary" 

# PyInstaller Location: C:\Python37\Scripts

pyinstaller --onefile --clean --windowed --add-data "C:/Users/iMukesh/Desktop/TGramBot-master/telegram/gui/ui/form.ui;." telegram/gui/telegram_gui.py

# pyinstaller telegram_gui.spec

PAUSE