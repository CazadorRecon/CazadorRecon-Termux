#!/usr/bin/env python3
"""
CazadorRecon v21.0 - Con TikTok OSINT + Web Downloader (HTTrack)
"""

import os
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

import subprocess
import time
import random
import requests
import re
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
RESULT_DIR = SCRIPT_DIR / "results"
RESULT_DIR.mkdir(exist_ok=True)

for folder in ["sherlock", "maigret", "whatsapp", "telegram", "tiktok", "websites"]:
    (RESULT_DIR / folder).mkdir(exist_ok=True)

PROXIES_FILE = Path("proxies.txt")

def load_proxies():
    if PROXIES_FILE.exists():
        with open(PROXIES_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

def get_session(proxy=None, use_tor=False):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    if use_tor:
        session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    elif proxy:
        session.proxies = {'http': proxy, 'https': proxy}
    return session

def random_delay():
    time.sleep(random.uniform(1.5, 3.5))

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"[!] Error: {e}")

def tiktok_osint():
    username = input("Usuario de TikTok (sin @): ").strip()
    print(f"\n[+] Buscando en TikTok: @{username}")
    url = f"https://www.tiktok.com/@{username}"
    print(f"[+] URL: {url}")
    print("[i] Abre el enlace manualmente o usa un navegador.")

def web_downloader():
    url = input("\nIngresa la URL del sitio web: ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    folder_name = input("Nombre de la carpeta para guardar el sitio: ").strip()
    if not folder_name:
        folder_name = "website_" + str(int(time.time()))

    output_path = RESULT_DIR / "websites" / folder_name

    print(f"\n[+] Descargando sitio web con HTTrack...")
    print(f"[+] URL: {url}")
    print(f"[+] Guardando en: {output_path}")

    cmd = f'httrack "{url}" -O "{output_path}" --depth=3 --ext-depth=3'
    run_command(cmd)
    print(f"\n[OK] Sitio descargado en: {output_path}")

def text_menu():
    print("\nCazadorRecon v21.0 | Con Web Downloader\n")
    while True:
        print("="*55)
        print("1. Sherlock")
        print("2. Maigret")
        print("3. WhatsApp OSINT")
        print("4. Telegram OSINT")
        print("5. TikTok OSINT")
        print("6. Web Downloader (HTTrack)")
        print("7. Info de Telefono")
        print("8. Salir")
        print("="*55)

        choice = input("\nOpcion (1-8): ").strip()

        if choice == "1":
            username = input("Username: ")
            run_command(f"sherlock {username} --timeout 15")
        elif choice == "2":
            username = input("Username: ")
            run_command(f"maigret {username} --timeout 15")
        elif choice == "3":
            phone = input("Telefono (+): ")
            print("[i] Funcion de WhatsApp aqui...")
        elif choice == "4":
            user = input("Usuario Telegram: ")
            print("[i] Funcion de Telegram aqui...")
        elif choice == "5":
            tiktok_osint()
        elif choice == "6":
            web_downloader()
        elif choice == "7":
            phone = input("Telefono: ")
            run_command(f"python -c 'import phonenumbers; from phonenumbers import geocoder, carrier; p=phonenumbers.parse(\"{phone}\"); print(geocoder.description_for_number(p,\"es\")); print(carrier.name_for_number(p,\"es\"))'")
        elif choice == "8":
            print("Finalizado.")
            break

if __name__ == "__main__":
    text_menu()