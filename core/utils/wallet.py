import os
import base64
import requests
from decimal import Decimal
from datetime import datetime
from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from Crypto.Cipher import AES
from eth_account import Account
from web3 import Web3

# --- 私钥加密 ---
def encrypt_private_key(private_key: str, secret_key: str) -> str:
    iv = os.urandom(16)
    cipher = AES.new(secret_key.encode('utf-8'), AES.MODE_CFB, iv=iv)
    encrypted = iv + cipher.encrypt(private_key.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# --- 钱包生成 ---
def generate_wallet_for_user(chain: str, token: str, secret_key: str):
    if chain.lower() == 'erc20':
        acct = Account.create()
        return {
            'address': acct.address,
            'private_key': encrypt_private_key(acct.key.hex(), secret_key)
        }
    elif chain.lower() == 'trc20':
        client = Tron()
        acct = client.generate_address()
        return {
            'address': acct['base58check_address'],
            'private_key': encrypt_private_key(acct['private_key'], secret_key)
        }
    else:
        raise ValueError("Unsupported chain")

# --- TRON 查询主币余额 ---
def get_trx_balance(address: str) -> float:
    try:
        client = Tron()
        return float(client.get_account_balance(address))
    except AddressNotFound:
        return 0.0
    except Exception:
        return 0.0

# --- TRC20 USDT 查询 ---
def get_usdt_trc20_balance(address: str) -> float:
    try:
        client = Tron()
        contract = client.get_contract("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
        balance = contract.functions.balanceOf(address)
        return float(balance) / 1_000_000
    except Exception:
        return 0.0

# --- ETH 主币查询 ---
def get_eth_balance(address: str) -> float:
    try:
        w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
        balance_wei = w3.eth.get_balance(Web3.to_checksum_address(address))
        return float(w3.from_wei(balance_wei, 'ether'))
    except Exception:
        return 0.0

# --- ERC20 USDT 查询 ---
def get_usdt_erc20_balance(address: str) -> float:
    try:
        w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
        usdt_contract = w3.eth.contract(
            address=Web3.to_checksum_address("0xdAC17F958D2ee523a2206206994597C13D831ec7"),
            abi=[{
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }]
        )
        balance = usdt_contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
        return balance / 1_000_000
    except Exception:
        return 0.0

# --- TRC20 今日收入/支出 ---
def get_today_trx_stats(address: str) -> tuple[float, float]:
    try:
        TRONGRID_API_KEY = os.getenv("TRONGRID_API_KEY")
        now = datetime.utcnow()
        start_timestamp = int(datetime(now.year, now.month, now.day).timestamp() * 1000)

        url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
        params = {
            "only_confirmed": "true",
            "limit": 200,
            "min_timestamp": start_timestamp,
            "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        }
        headers = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        txs = resp.json().get("data", [])

        income, expense = Decimal("0"), Decimal("0")
        for tx in txs:
            value = Decimal(tx["value"]) / Decimal(1_000_000)
            if tx["to"] == address:
                income += value
            elif tx["from"] == address:
                expense += value

        return float(income), float(expense)
    except Exception:
        return 0.0, 0.0

# --- ERC20 收支统计：占位 ---
def get_today_erc_stats(address: str) -> tuple[float, float]:
    # TODO: 可接入 Etherscan API 获取 ERC20 Transfer 记录
    return 0.0, 0.0

from asgiref.sync import sync_to_async
from decimal import Decimal
from datetime import datetime
from django.db.models import Sum
from core.models import RechargeLog

@sync_to_async
def get_today_usdt_stats(address: str):
    today = datetime.now().date()

    incomes = RechargeLog.objects.filter(
        wallet__address=address,
        token_type="USDT",
        created_at__date=today
    ).aggregate(Sum("amount"))["amount__sum"] or Decimal("0")

    # 暂时没有支出表，因此直接设为 0
    outcomes = Decimal("0")

    profit = incomes - outcomes

    return {
        "income": float(incomes),
        "outcome": float(outcomes),
        "profit": float(profit)
    }