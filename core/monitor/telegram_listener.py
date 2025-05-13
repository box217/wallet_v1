import os
import time
from decimal import Decimal
from django.utils import timezone
from core.models import TelegramWatchAddress
from core.utils.telegram import send_tg_message

# 👇 可扩展的监听函数
def check_erc20_transactions():
    from web3 import Web3
    INFURA_URL = os.getenv("INFURA_URL")
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    
    # 模拟链上监听：这里你应接入实际的 Web3 事件订阅
    for entry in TelegramWatchAddress.objects.filter(chain_type="erc20"):
        latest_balance = w3.eth.get_balance(entry.address)
        if latest_balance > 0:  # 简化逻辑
            send_tg_message(entry.chat_id, f"🔔 ERC20 地址收到转账：{latest_balance / 1e18:.6f} ETH\n地址：{entry.address}")

def check_trc20_transactions():
    from tronpy import Tron
    client = Tron()
    
    for entry in TelegramWatchAddress.objects.filter(chain_type="trc20"):
        balance = client.get_account_balance(entry.address)
        if balance > 0:
            send_tg_message(entry.chat_id, f"🔔 TRC20 地址收到转账：{Decimal(balance):.6f} TRX\n地址：{entry.address}")

def run_loop():
    while True:
        try:
            check_erc20_transactions()
            check_trc20_transactions()
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(15)