#!/usr/bin/env python3
"""
CazadorRecon v20.0 - Version limpia y estable para Termux
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

RESULT_DIR = Path("~/osint_results").expanduser()
RESULT_DIR.mkdir(exist_ok=True, parents=True)

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
    except Exception as e:
        print(f"[!] Error: {e}")

def phone_basic(phone):
    print(f"[+] Informacion del numero +{phone}")
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
    print(f"[+] Buscando en WhatsApp: +{phone}")
    try:
        session = get_session()
        random_delay()
        r = session.get(f"https://web.whatsapp.com/send?phone={phone}", timeout=20)
        if "invalid" in r.text.lower():
            print("[-] Numero no registrado en WhatsApp")
        else:
            print("[+] Numero encontrado en WhatsApp")
    except Exception as e:
        print(f"Error: {e}")

def telegram_osint(username):
    username = username.lstrip('@')
    print(f"[+] Buscando en Telegram: @{username}")
    try:
        session = get_session()
        random_delay()
        r = session.get(f"https://t.me/{username}", timeout=15)
        if "If you have Telegram" in r.text:
            print("[-] Usuario no encontrado")
        else:
            print("[+] Usuario encontrado en Telegram")
    except Exception as e:
        print(f"Error: {e}")

def run_sherlock(username):
    print(f"[+] Ejecutando Sherlock en @{username}...")
    run_command(f"sherlock {username} --timeout 15")

def run_maigret(username):
    print(f"[+] Ejecutando Maigret en @{username}...")
    run_command(f"maigret {username} --timeout 15")

def run_holehe(email):
    print(f"[+] Ejecutando Holehe en {email}...")
    run_command(f"holehe {email} --only-used")

def text_menu():
    proxies = load_proxies()
    print(f"\nCazadorRecon v20.0 | Proxies: {len(proxies)}\n")
    while True:
        print("="*60)
        print("                    CAZADORRECON v20.0")
        print("="*60)
        print("1. Sherlock")
        print("2. Maigret")
        print("3. Holehe (Email)")
        print("4. WhatsApp OSINT")
        print("5. Telegram OSINT")
        print("6. Info de Telefono")
        print("7. Salir")
        print("="*60)

        choice = input("\nOpcion (1-7): ").strip()

        if choice == '1':
            run_sherlock(input("Username: "))
        elif choice == '2':
            run_maigret(input("Username: "))
        elif choice == '3':
            run_holehe(input("Email: "))
        elif choice == '4':
            whatsapp_osint(input("Telefono (+): "))
        elif choice == '5':
            telegram_osint(input("Usuario Telegram: "))
        elif choice == '6':
            phone_basic(input("Telefono (+): "))
        elif choice == '7':
            print("Finalizado.")
            break

def main():
    parser = argparse.ArgumentParser(description="CazadorRecon v20.0")
    parser.add_argument('--menu', action='store_true')
    args = parser.parse_args()
    if args.menu or len(sys.argv) == 1:
        text_menu()

if __name__ == "__main__":
    main()