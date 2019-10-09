#!/usr/bin/env bash


echo "[+] Creating Virtual Env"
python3 -m venv .venv

echo "[+] Activating Virtual Env"
source .venv/bin/activate 

echo "[+] Installing Dependencies"
python3 -m pip install --no-cache-dir -r requirements.txt