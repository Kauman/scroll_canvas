from web3 import Web3, Account
import time
import random
import datetime
import requests
import json
import string

# BEFORE MINT THERE IS CHECK FOR HAVING PROFILE, SO NO WORRIES ABOUT THAT!
# ДО МИНТА ЕСТЬ ПРОВЕРКА НА НАЛИЧИЕ ПРОФИЛЯ, ПОЭТОМУ НЕ ПЕРЕЖИВАЙТЕ!

# WANT TO USE PROXY? | ПРОКСИ ВКЛЮЧИТЬ ИЛИ ВЫКЛЮЧИТЬ? add them to proxy.txt with FORMAT | IP:PORT:USERNAME:PASSWORD
PROXY = False
# WAIT FOR TX SUCCESS OR CONTINUE | ЖДАТЬ КОГДА ЕБАНЫЙ ЧЕЙН РАЗДУПЛИТСЯ ИЛИ ПРОСТО ПИЗДОВАТЬ ВПЕРЕД?
WAIT_FOR_SUCCESS = False
# SLEEP BETWEEN ACCOUNTS | СОН МЕЖДУ АККАМИ
SLEEP = 10, 30

# CHANGE RPC IF YOU WANT | НЕ ТРОГАЙ, СЫНОК, ЕБАНЕТ, РАЗВЕ ЧТО RPC_SCROLL.
RPC_SCROLL = 'https://scroll.drpc.org'

# IF YOU ARE SMART, YOU CAN TRY TO ADD NEW NAMES (IT'S BASE NAME THEN THERE IS SOME RANDOM CHANGES WILL BE APPLIED TO THEM), SO NO WORRY AGAIN, EVERYTHING IS UNIQUE.
# ЕСЛИ ВЫ ДОХУЯ УМНЫЙ И ОСОЗНАЕТЕ ЧТО ДЕЛАЕТЕ, ТО МОЖЕТЕ ПОДОБАВЛЯТЬ СВОИ ИМЕНА (ЭТО БАЗА И ИМЕНА ВСЕ РАВНО БУДУТ ИЗМЕНЕНЫ И РАНДОМИЗИРОВАНЫ ПРИ РЕГЕ, ЧТОБЫ ВСЕ БЫЛО УНИКАЛЬНО).
base_names = [
    "Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Hannah", "Ivy", "Jack",
    "Katherine", "Liam", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Rachel", "Sophia", "Tom",
    "Uma", "Vera", "William", "Xena", "Yara", "Zane", "KFC", "MCDONALDS", 'Degen', 'Huesos', 'Pedro', 'Ebaklak', 'Friend', 'Donald', 'Trump', 'Biden',
    "Daun", 'Clown', 'Homunculus', 'Sabaka', 'Christiano', 'Racer', 'Flamingo', 'Skoobidoo', 'Papandos', 'Dikiy', 'Uganda',
]

# DONT TOUCH | НУ ЭТО ТОЧНО НЕ НУЖНО ТРОГАТЬ!
SCROLL_CHAIN_ID = 534352
CONTRACT_ADDRESS = '0xB23AF8707c442f59BDfC368612Bd8DbCca8a7a5a'
CONTRACT_ABI = '''[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"CallerIsNotUserProfile","type":"error"},{"inputs":[],"name":"DuplicatedUsername","type":"error"},{"inputs":[],"name":"ExpiredSignature","type":"error"},{"inputs":[],"name":"ImplementationNotContract","type":"error"},{"inputs":[],"name":"InvalidReferrer","type":"error"},{"inputs":[],"name":"InvalidSignature","type":"error"},{"inputs":[],"name":"InvalidUsername","type":"error"},{"inputs":[],"name":"MsgValueMismatchWithMintFee","type":"error"},{"inputs":[],"name":"ProfileAlreadyMinted","type":"error"},{"anonymous":false,"inputs":[],"name":"EIP712DomainChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"profile","type":"address"},{"indexed":true,"internalType":"address","name":"referrer","type":"address"}],"name":"MintProfile","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"profile","type":"address"},{"indexed":false,"internalType":"string","name":"username","type":"string"}],"name":"RegisterUsername","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"profile","type":"address"},{"indexed":false,"internalType":"string","name":"username","type":"string"}],"name":"UnregisterUsername","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"oldAvatar","type":"string"},{"indexed":false,"internalType":"string","name":"newAvatar","type":"string"}],"name":"UpdateDefaultProfileAvatar","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldImplementation","type":"address"},{"indexed":true,"internalType":"address","name":"newImplementation","type":"address"}],"name":"UpdateProfileImplementation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldSigner","type":"address"},{"indexed":true,"internalType":"address","name":"newSigner","type":"address"}],"name":"UpdateSigner","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldTreasury","type":"address"},{"indexed":true,"internalType":"address","name":"newTreasury","type":"address"}],"name":"UpdateTreasury","type":"event"},{"inputs":[],"name":"MINT_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"hashes","type":"bytes32[]"}],"name":"blacklistUsername","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cloneableProxyHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"eip712Domain","outputs":[{"internalType":"bytes1","name":"fields","type":"bytes1"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"version","type":"string"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"verifyingContract","type":"address"},{"internalType":"bytes32","name":"salt","type":"bytes32"},{"internalType":"uint256[]","name":"extensions","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDefaultProfileAvatar","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getProfile","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"treasury_","type":"address"},{"internalType":"address","name":"signer_","type":"address"},{"internalType":"address","name":"profileImpl_","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isProfileMinted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"username","type":"string"}],"name":"isUsernameUsed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"username","type":"string"},{"internalType":"bytes","name":"referral","type":"bytes"}],"name":"mint","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"referrerData","outputs":[{"internalType":"uint128","name":"referred","type":"uint128"},{"internalType":"uint128","name":"earned","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"username","type":"string"}],"name":"registerUsername","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"signer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"treasury","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"username","type":"string"}],"name":"unregisterUsername","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newAvatar","type":"string"}],"name":"updateDefaultProfileAvatar","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"updateProfileImplementation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newSigner","type":"address"}],"name":"updateSigner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newTreasury","type":"address"}],"name":"updateTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"}]'''
scanner_link = 'https://scrollscan.com/tx/'

with open('private_keys.txt', 'r') as file:
    private_keys = [line.strip() for line in file]

with open('proxy.txt', 'r') as proxy_file:
    proxies = [line.strip() for line in proxy_file]


def modify_name(name):
    modified_name = ""
    for char in name:
        if random.random() < 0.2:
            modified_name += random.choice(string.ascii_letters)
        else:
            modified_name += char
    insert_position = random.randint(0, len(modified_name))
    modified_name = modified_name[:insert_position] + modified_name[insert_position:]

    return modified_name


def generate_human_like_name():
    base_name = random.choice(base_names)
    return modify_name(base_name)


def get_signature(wallet):
    url = f"https://canvas.scroll.cat/code/6CC2Z/sig/{wallet}"
    headers = {
        "Host": "canvas.scroll.cat",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Accept-Language": "en-EN",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://scroll.io",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://scroll.io/",
        "Priority": "u=1, i"
    }
    try:
        if PROXY is True:
            response = requests.get(url, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        signature = data.get("signature")
        return signature
    except Exception as e:
        print(e)


def check_minted():
    contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
    getprofile = contract.functions.getProfile(account.address).call()
    is_claimed = contract.functions.isProfileMinted(getprofile).call()
    print(f"CANVAS Profile already minted!", is_claimed)
    return is_claimed


def mint_shit():
    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
        random_name = generate_human_like_name()
        signature = get_signature(account.address)
        tx = contract.functions.mint(random_name, signature).build_transaction({
            'chainId': SCROLL_CHAIN_ID,
            'gas': random.randint(500000, 550000),
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(w3.to_checksum_address(account.address)),
            'value': w3.to_wei(0.0005, 'ether'),
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"SIGNED TX: {tx_hash.hex()} (pending...)")
        if WAIT_FOR_SUCCESS is False:
            return 1
        else:
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            success = receipt['status']
            link_to_scan = scanner_link + tx_hash.hex()
        if success == 1:
            print(f"SUCCESS MINT! | TX: {link_to_scan}")
            return success
        else:
            print(f"FAIL MINT! | TX: {link_to_scan}")
    except Exception as e:
        print(e)

num = 0
if not proxies and PROXY is True:
    print("NO PROXIES IN PROXY.TXT | Файл с прокси пуст или не содержит прокси.")
    print("PROXY = False or add proxy | PROXY = False или добавьте прокси")
    input("чини...")
if PROXY is True:
    print(f"PROXY MODE")
    for private_key, proxy_info in zip(private_keys, proxies):
        proxy_ip, port, username, password = proxy_info.split(":")
        if username == 'PweFh8Mc':  # FIX SOCKS TO HTTP
            newport = int(port) - 1
            proxy_url = f"http://{username}:{password}@{proxy_ip}:{newport}"
        else:
            proxy_url = f"http://{username}:{password}@{proxy_ip}:{port}"
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        num += 1
        w3 = Web3(Web3.HTTPProvider(endpoint_uri=RPC_SCROLL, request_kwargs={"proxies": {'https': proxy_url, 'http': proxy_url}}))
        account = Account.from_key(private_key)
        address = account.address
        tx_count = w3.eth.get_transaction_count(address)
        balance = w3.from_wei(w3.eth.get_balance(address), 'ether')
        print(f"№{num} | {address} | TX: {tx_count} | {balance} | PROXY: {proxy_ip}")
        is_minted = check_minted()
        if is_minted is True:
            continue
        else:
            success = mint_shit()
            if success == 1:
                print(f"SLEEP.... zZz...Zzz...")
                time.sleep(random.randint(SLEEP[0], SLEEP[1]))
else:
    print(f"WITHOUT PROXY")
    for private_key in private_keys:
        num += 1
        w3 = Web3(Web3.HTTPProvider(RPC_SCROLL))
        account = Account.from_key(private_key)
        address = account.address
        tx_count = w3.eth.get_transaction_count(address)
        balance = w3.from_wei(w3.eth.get_balance(address), 'ether')
        print(f"№{num} | {address} | TX: {tx_count} | {balance} | WITHOUT PROXY")
        is_minted = check_minted()
        if is_minted is True:
            continue
        else:
            success = mint_shit()
            if success == 1:
                print(f"SLEEP.... zZz...Zzz...")
                time.sleep(random.randint(SLEEP[0], SLEEP[1]))
