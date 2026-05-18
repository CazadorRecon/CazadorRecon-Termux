#!/usr/bin/env python3
"""
CazadorRecon v20.4 - Con TikTok OSINT
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

# Subcarpetas
for tool in ["sherlock", "maigret", "whatsapp", "telegram", "holehe", "tiktok"]:
    (RESULT_DIR / tool).mkdir(exist_ok=True)

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
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
        print(result.stdout.strip())
        return result.stdout.strip()
    except Exception as e:
        print(f"[!] Error: {e}")
        return ""

def phone_basic(phone):
    print(f"\n[+] Informacion del numero +{phone}")
    try:
        import phonenumbers
        from phonenumbers import geocoder, carrier
        p = phonenumbers.parse(phone)
        print("Pais:", geocoder.description_for_number(p, "es"))
        print("Operadora:", carrier.name_for_number(p, "es"))
    except:
        print("[-] No se pudo analizar el numero")

def whatsapp_osint(phone):
    phone = phone.lstrip('+')
    print(f"\n[+] Buscando en WhatsApp: +{phone}")
    try:
        session = get_session()
        random_delay()
        r = session.get(f"https://web.whatsapp.com/send?phone={phone}", timeout=25)
        if r.status_code != 200 or "invalid" in r.text.lower():
            print("❌ Este numero NO tiene WhatsApp")
            return
        print("✅ Este numero TIENE WhatsApp")
        filename = RESULT_DIR / "whatsapp" / f"{phone}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Numero: +{phone}\nTiene WhatsApp: Si\n")
        print(f"[OK] Guardado en results/whatsapp/{phone}.txt")
    except Exception as e:
        print(f"Error: {e}")

def telegram_osint(username):
    username = username.lstrip('@')
    print(f"\n[+] Buscando en Telegram: @{username}")
    try:
        session = get_session()
        random_delay()
        r = session.get(f"https://t.me/{username}", timeout=15)
        if "If you have Telegram" in r.text:
            print("❌ Usuario no encontrado")
            return
        print("✅ Usuario encontrado en Telegram")
        filename = RESULT_DIR / "telegram" / f"{username}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Usuario: @{username}\n")
        print(f"[OK] Guardado en results/telegram/{username}.txt")
    except Exception as e:
        print(f"Error: {e}")

def tiktok_osint(username):
    username = username.lstrip('@')
    print(f"\n[+] Buscando en TikTok: @{username}")
    try:
        session = get_session()
        random_delay()
        url = f"https://www.tiktok.com/@{username}"
        r = session.get(url, timeout=15)
        if r.status_code == 200 and "Couldn't find this account" not in r.text:
            print("✅ Usuario encontrado en TikTok")
            filename = RESULT_DIR / "tiktok" / f"{username}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Usuario: @{username}\nURL: {url}\n")
            print(f"[OK] Guardado en results/tiktok/{username}.txt")
        else:
            print("❌ Usuario no encontrado en TikTok")
    except Exception as e:
        print(f"Error: {e}")

def run_sherlock(username):
    print(f"\n[+] Ejecutando Sherlock en @{username}...")
    output = run_command(f"sherlock {username} --timeout 15")
    filename = RESULT_DIR / "sherlock" / f"{username}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"[OK] Guardado en results/sherlock/{username}.txt")

def run_maigret(username):
    print(f"\n[+] Ejecutando Maigret en @{username}...")
    output = run_command(f"maigret {username} --timeout 15")
    filename = RESULT_DIR / "maigret" / f"{username}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"[OK] Guardado en results/maigret/{username}.txt")

def run_holehe(email):
    print(f"\n[+] Ejecutando Holehe en {email}...")
    output = run_command(f"holehe {email} --only-used")
    filename = RESULT_DIR / "holehe" / f"{email.replace('@','_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"[OK] Guardado en results/holehe/{email.replace('@','_')}.txt")

def text_menu():
    print(f"\nCazadorRecon v20.4 | Con TikTok OSINT\n")
    while True:
        print("="*60)
        print("                    CAZADORRECON v20.4")
        print("="*60)
        print("1. Sherlock     2. Maigret")
        print("3. Holehe       4. WhatsApp OSINT")
        print("5. Telegram     6. TikTok OSINT")
        print("7. Info Telefono 8. Salir")
        print("="*60)
        choice = input("\nOpcion (1-8): ").strip()
        if choice == '1': run_sherlock(input("Username: "))
        elif choice == '2': run_maigret(input("Username: "))
        elif choice == '3': run_holehe(input("Email: "))
        elif choice == '4': whatsapp_osint(input("Telefono (+): "))
        elif choice == '5': telegram_osint(input("Usuario Telegram: "))
        elif choice == '6': tiktok_osint(input("Usuario TikTok: "))
        elif choice == '7': phone_basic(input("Telefono (+): "))
        elif choice == '8': break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--menu', action='store_true')
    args = parser.parse_args()
    if args.menu or len(sys.argv) == 1:
        text_menu()

if __name__ == "__main__":
    main()