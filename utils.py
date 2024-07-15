import time
import random
import requests

from config import *

def pick_and_remove_name(address: str):
    chosen_name = random.choice(base_names)
    base_names.remove(chosen_name)
    with open("data\used_names.txt", "a") as file:
        file.write(f"{address}:{chosen_name}\n")
    return chosen_name

def change_ip():
    if CHANGE_IP_LINK not in ['https://changeip.mobileproxy.space/?proxy_key=...&format=json', '']:
        while True:
            try:
                r = requests.get(CHANGE_IP_LINK)
                if not 'mobileproxy' in CHANGE_IP_LINK and r.status_code == 200:
                    print(f'[+] Proxy | Successfully changed ip: {r.text}')
                    return True
                print(f'[-] Proxy | Change IP error: {r.text} | {r.status_code}')
                time.sleep(10)
            except Exception as err:
                print(f'[-] Browser | Cannot get proxy: {err}')
    
def end_actions():
    print(f"SLEEP.... zZz...Zzz...")
    time.sleep(random.randint(SLEEP[0], SLEEP[1]))
    if MOBILE_PROXY != "":
        change_ip()