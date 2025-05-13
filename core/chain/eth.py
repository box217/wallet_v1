from web3 import Web3
import os
from eth_account import Account
from decimal import Decimal
from dotenv import load_dotenv
import json

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")  # 放 .env 中
ERC20_ABI = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"}]')

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
assert web3.is_connected(), "无法连接 Infura 节点"

def get_token_balance(token_address, user_address):
    contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    balance = contract.functions.balanceOf(Web3.to_checksum_address(user_address)).call()
    return Decimal(balance) / Decimal(1e6)  # 默认6位精度

def transfer_token(token_address, private_key, to_address, amount):
    acct = Account.from_key(private_key)
    contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    nonce = web3.eth.get_transaction_count(acct.address)

    tx = contract.functions.transfer(
        Web3.to_checksum_address(to_address),
        int(amount * 1e6)
    ).build_transaction({
        'chainId': 1,
        'gas': 100000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': nonce
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

def transfer_eth(private_key, to_address, amount):
    acct = Account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(acct.address)

    tx = {
        'to': Web3.to_checksum_address(to_address),
        'value': web3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': nonce,
        'chainId': 1
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()
