import os
import time
import json
import requests
import itertools
from decimal import Decimal
from django.core.management.base import BaseCommand
from core.models import TelegramWatchAddress, RechargeLog
from core.utils.tg_notify import send_tg_message
from core.utils.wallet import get_trx_balance, get_usdt_trc20_balance, get_token_balance, get_today_trx_stats

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../../monitor_config.json")
with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

TOKENS = CONFIG["tokens"]
API_KEYS = CONFIG["api_keys"]
KEY_CYCLE = itertools.cycle(API_KEYS)
POLL_INTERVAL = CONFIG.get("polling_interval", 30)
BATCH_SIZE = CONFIG.get("batch_size", 10)


def get_headers():
    return {"TRON-PRO-API-KEY": next(KEY_CYCLE)}

def get_trx_cost(tx_id: str, headers: dict):
    url = f"https://api.trongrid.io/wallet/gettransactioninfobyid"
    try:
        resp = requests.post(url, json={"value": tx_id}, headers=headers, timeout=10)
        data = resp.json()
        energy_usage = data.get("energy_usage_total", 0)
        bandwidth_usage = data.get("net_usage", 0)
        fee = Decimal(data.get("fee", 0)) / Decimal(1_000_000)
        return {
            "energy": energy_usage,
            "bandwidth": bandwidth_usage,
            "fee": fee,
        }
    except Exception:
        return {
            "energy": 0,
            "bandwidth": 0,
            "fee": Decimal("0.0"),
        }

class Command(BaseCommand):
    help = "监听 TRC20 地址收入"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 正在监听 TRC20 地址收入...")
        while True:
            try:
                watches = TelegramWatchAddress.objects.filter(chain_type="trc20")
                for watch in watches:
                    for symbol, token in TOKENS.items():
                        try:
                            url = (
                                f"https://api.trongrid.io/v1/accounts/{watch.address}/transactions/trc20"
                                f"?only_confirmed=true&limit=5&contract_address={token['contract']}"
                            )
                            resp = requests.get(url, headers=get_headers(), timeout=10)
                            data = resp.json()
                            if "data" not in data:
                                continue

                            for tx in data["data"]:
                                if tx["to"].lower() != watch.address.lower():
                                    continue
                                tx_hash = tx["transaction_id"]
                                if RechargeLog.objects.filter(tx_hash=tx_hash).exists():
                                    continue

                                amount = Decimal(tx["value"]) / Decimal(10 ** token["decimals"])
                                from_address = tx["from"]
                                to_address = tx["to"]
                                timestamp = int(tx["block_timestamp"]) // 1000
                                dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

                                cost = get_trx_cost(tx_hash, get_headers())
                                balance_usdt = get_token_balance(watch.address, symbol)
                                balance_trx = get_trx_balance(watch.address)
                                stats = get_today_trx_stats(watch.address)

                                message = (
                                    f"🟢收入{symbol} 提醒       +{amount} {symbol}\n\n"
                                    f"地址备注: \n\n"
                                    f"付款地址: {from_address}\n"
                                    f"收款地址: {to_address}\n"
                                    f"交易时间:    {dt}\n"
                                    f"交易金额:    +{amount} {symbol}\n"
                                    f"{symbol}余额:  {balance_usdt:.6f} {symbol}\n"
                                    f"TRX余额:   {balance_trx:.6f} TRX\n"
                                    f"转账消耗: {cost['fee']} TRX; {cost['bandwidth']} 带宽; {cost['energy']} 能量\n\n"
                                    f"今日收入: {stats[0]} {symbol}\n"
                                    f"今日支出: {stats[1]} {symbol}\n"
                                    f"今日利润: {stats[0] - stats[1]} {symbol}\n\n"
                                    f"[🔍查看交易详情](https://tronscan.org/#/transaction/{tx_hash})"
                                )

                                send_tg_message(watch.chat_id, message)

                                RechargeLog.objects.create(
                                    wallet=None,
                                    tx_hash=tx_hash,
                                    amount=amount,
                                    confirmed=True,
                                    chain_type="TRC20",
                                    token_type=symbol,
                                )

                        except Exception as e:
                            self.stdout.write(f"❌ 地址 {watch.address} 监听失败: {str(e)}")
                time.sleep(POLL_INTERVAL)
            except KeyboardInterrupt:
                self.stdout.write("🛑 监听已终止")
                break
