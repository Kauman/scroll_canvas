import time
import random
import requests
import json

from web3 import Web3, Account

import utils
from config import *


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
        random_name = utils.pick_and_remove_name(address)

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
        
        
        
index = 0
    
if PROXY is True:
    print(f"PROXY MODE")
    if MOBILE_PROXY != "" and CHANGE_IP_LINK != "": proxies = [MOBILE_PROXY] * len(private_keys) 
    for private_key, proxy_info in zip(private_keys, proxies):
        proxies = {
            'http': f"http://{proxy_info}",
            'https': f"http://{proxy_info}"
        }
        index += 1
        
        w3 = Web3(Web3.HTTPProvider(
            endpoint_uri=RPC_SCROLL, 
            request_kwargs={
                "proxies": {
                    'https': f"http://{proxy_info}", 
                    'http': f"http://{proxy_info}"
                }
            }
        ))
        
        account = Account.from_key(private_key)
        address = account.address
        tx_count = w3.eth.get_transaction_count(address)
        balance = w3.from_wei(w3.eth.get_balance(address), 'ether')
        print(f"№{index} | {address} | TX: {tx_count} | {balance} | PROXY: {proxy_info}")
        if balance < w3.to_wei(0.001, "ether"):
            print("Balance less than 0.001 ETH for mint Scroll Canvas")
            print("sleeping before next acc")
            
        is_minted = check_minted()
        if is_minted is not True:
            success = mint_shit()
        utils.end_actions()
                
            
else:
    print(f"WITHOUT PROXY")
    for private_key in private_keys:
        index += 1
        w3 = Web3(Web3.HTTPProvider(RPC_SCROLL))
        account = Account.from_key(private_key)
        address = account.address
        tx_count = w3.eth.get_transaction_count(address)
        balance = w3.from_wei(w3.eth.get_balance(address), 'ether')
        print(f"№{index} | {address} | TX: {tx_count} | {balance} | WITHOUT PROXY")
        
        is_minted = check_minted()
        if is_minted is not True:
            success = mint_shit()
        utils.end_actions()