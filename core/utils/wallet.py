import os
import base64
import requests
import json
import itertools
from decimal import Decimal
from datetime import datetime
from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from Crypto.Cipher import AES
from eth_account import Account
from web3 import Web3
from asgiref.sync import sync_to_async
from django.db.models import Sum
from core.models import RechargeLog

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

# --- TRON 主币余额查询 ---
def get_trx_balance(address: str) -> float:
    try:
        client = Tron()
        return float(client.get_account_balance(address))
    except AddressNotFound:
        return 0.0
    except Exception:
        return 0.0

# --- TRC20 USDT 余额 ---
def get_usdt_trc20_balance(address: str) -> float:
    try:
        client = Tron()
        contract = client.get_contract("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
        balance = contract.functions.balanceOf(address)
        return float(balance) / 1_000_000
    except Exception:
        return 0.0

# --- TRC20 USDD 余额 ---
def get_usdd_trc20_balance(address: str) -> float:
    try:
        client = Tron()
        contract = client.get_contract("TXDk8mbtRbXeYuMNS83CfKPaYYT8XWv9Hz")
        balance = contract.functions.balanceOf(address)
        return float(balance) / 1_000_000_000_000_000_000
    except Exception:
        return 0.0

# --- ETH 主币余额 ---
def get_eth_balance(address: str) -> float:
    try:
        w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
        balance_wei = w3.eth.get_balance(Web3.to_checksum_address(address))
        return float(w3.from_wei(balance_wei, 'ether'))
    except Exception:
        return 0.0
# --- 查询 BTC 地址余额函数---
def get_btc_balance(address: str) -> float:
    try:
        url = f"https://blockstream.info/api/address/{address}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        confirmed = data.get("chain_stats", {}).get("funded_txo_sum", 0)
        spent = data.get("chain_stats", {}).get("spent_txo_sum", 0)
        balance = (confirmed - spent) / 1e8  # Satoshis to BTC
        return balance
    except Exception:
        return 0.0

# --- ERC20 USDT 余额 ---
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
        config_path = os.path.join(os.path.dirname(__file__), "../../monitor_config.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        api_keys = itertools.cycle(config.get("api_keys", []))

        now = datetime.utcnow()
        start_timestamp = int(datetime(now.year, now.month, now.day).timestamp() * 1000)

        url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
        params = {
            "only_confirmed": "true",
            "limit": 200,
            "min_timestamp": start_timestamp,
            "contract_address": config["tokens"]["USDT"]["contract"]
        }
        headers = {"TRON-PRO-API-KEY": next(api_keys)}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        txs = resp.json().get("data", [])

        income, expense = Decimal("0"), Decimal("0")
        for tx in txs:
            value = Decimal(tx["value"]) / Decimal(10 ** config["tokens"]["USDT"]["decimals"])
            if tx["to"].lower() == address.lower():
                income += value
            elif tx["from"].lower() == address.lower():
                expense += value

        return float(income), float(expense)
    except Exception:
        return 0.0, 0.0

# --- ERC20 收支统计占位 ---
def get_today_erc_stats(address: str) -> tuple[float, float]:
    return 0.0, 0.0

@sync_to_async
def get_today_usdt_stats(address: str):
    today = datetime.now().date()
    incomes = RechargeLog.objects.filter(
        wallet__address=address,
        token_type="USDT",
        created_at__date=today
    ).aggregate(Sum("amount"))["amount__sum"] or Decimal("0")

    outcomes = Decimal("0")
    profit = incomes - outcomes

    return {
        "income": float(incomes),
        "outcome": float(outcomes),
        "profit": float(profit)
    }

def get_token_balance(address, token_symbol):
    if token_symbol == "USDT":
        return get_usdt_trc20_balance(address)
    if token_symbol == "USDD":
        return get_usdd_trc20_balance(address)
    return Decimal("0.0")


from datetime import datetime
import requests
from decimal import Decimal

def get_today_btc_stats(address: str) -> tuple[float, float]:
    """
    获取 BTC 地址今日的收入和支出（使用 Blockstream API）。
    :param address: BTC 地址
    :return: (income, expense) 元组，单位为 BTC
    """
    try:
        # 获取当前日期起始时间戳（UTC）
        today = datetime.utcnow().date()
        base_url = f"https://blockstream.info/api/address/{address}/txs"
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        txs = response.json()

        income = Decimal("0")
        expense = Decimal("0")

        for tx in txs:
            timestamp = tx.get("status", {}).get("block_time")
            if not timestamp:
                continue

            tx_date = datetime.utcfromtimestamp(timestamp).date()
            if tx_date != today:
                continue

            # 判断是否支出
            total_sent = sum(
                Decimal(vin["prevout"]["value"]) for vin in tx.get("vin", [])
                if vin.get("prevout", {}).get("scriptpubkey_address") == address
            ) / Decimal(1e8)

            # 判断是否收入
            total_received = sum(
                Decimal(vout["value"]) for vout in tx.get("vout", [])
                if vout.get("scriptpubkey_address") == address
            ) / Decimal(1e8)

            income += total_received
            expense += total_sent

        return float(income), float(expense)

    except Exception:
        return 0.0, 0.0