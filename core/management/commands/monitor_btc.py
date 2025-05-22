
import os
import time
import requests
from decimal import Decimal
from django.core.management.base import BaseCommand
from core.models import TelegramWatchAddress, RechargeLog
from core.utils.tg_notify import send_tg_message

BLOCKSTREAM_API = "https://blockstream.info/api"

class Command(BaseCommand):
    help = "监听 BTC 地址收支情况"

    def handle(self, *args, **options):
        self.stdout.write("🚀 正在监听 BTC 地址收入和支出...")

        while True:
            try:
                watches = TelegramWatchAddress.objects.filter(chain_type="btc")
                for watch in watches:
                    try:
                        addr = watch.address
                        url = f"{BLOCKSTREAM_API}/address/{addr}/txs"
                        resp = requests.get(url, timeout=10)
                        txs = resp.json()

                        for tx in txs:
                            txid = tx["txid"]
                            if RechargeLog.objects.filter(tx_hash=txid).exists():
                                continue

                            # 计算该地址在本交易中为输入还是输出
                            is_income = any(addr == vout.get("scriptpubkey_address") for vout in tx["vout"])
                            is_expense = any(addr == vin.get("prevout", {}).get("scriptpubkey_address") for vin in tx["vin"])

                            if not is_income and not is_expense:
                                continue

                            amount = 0
                            if is_income:
                                for vout in tx["vout"]:
                                    if vout.get("scriptpubkey_address") == addr:
                                        amount += vout["value"]
                            elif is_expense:
                                for vin in tx["vin"]:
                                    prevout = vin.get("prevout", {})
                                    if prevout.get("scriptpubkey_address") == addr:
                                        amount -= prevout["value"]

                            btc_amount = Decimal(amount) / Decimal(100_000_000)
                            direction = "收入" if is_income else "支出"
                            emoji = "🟢" if is_income else "🔴"
                            symbol = "+" if is_income else "-"

                            RechargeLog.objects.create(
                                wallet=None,
                                tx_hash=txid,
                                amount=abs(btc_amount),
                                confirmed=True,
                                chain_type="BTC",
                                token_type="BTC",
                            )

                            msg = (
                                f"{emoji}{direction}BTC 提醒       {symbol}{abs(btc_amount)} BTC\n\n"
                                f"地址备注: \n\n"
                                f"地址: {addr}\n"
                                f"交易哈希: {txid}\n"
                                f"[🔍查看交易详情](https://blockstream.info/tx/{txid})"
                            )

                            send_tg_message(watch.chat_id, msg, parse_mode="Markdown")

                    except Exception as e:
                        self.stdout.write(f"⚠️ 地址 {watch.address} 监听异常: {e}")

                time.sleep(60)  # 可根据需要调整轮询频率

            except KeyboardInterrupt:
                self.stdout.write("🛑 BTC 监听终止")
                break
