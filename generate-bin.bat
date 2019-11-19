ECHO OFF

# Pre-requisite: python3 -m pip install pyinstaller

ECHO "[+] Generating Binary" 
# pyinstaller --onefile --windowed telegram/gui/telegram_gui.py
# --onedir for DEBUG

# PyInstaller Location: C:\Python37\Scripts

CURRENT_DIR="$(pwd)"

pyinstaller --onefile --clean --windowed \
            --add-data "${CURRENT_DIR}/telegram/gui/ui/form.ui:." \
            telegram/gui/telegram_gui.py 

# pyinstaller telegram_gui.spec

PAUSE