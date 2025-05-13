import os
import time
import requests
from decimal import Decimal
from django.core.management.base import BaseCommand
from core.models import TelegramWatchAddress, RechargeLog
from core.utils.tg_notify import send_tg_message

TRONGRID_API_KEY = os.getenv("TRONGRID_API_KEY")
HEADERS = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

class Command(BaseCommand):
    help = "监听 TRC20 地址 USDT 收款"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 正在监听 TRC20 地址收入...")

        while True:
            try:
                watches = TelegramWatchAddress.objects.filter(chain_type="trc20")
                for watch in watches:
                    try:
                        url = (
                            f"https://api.trongrid.io/v1/accounts/{watch.address}/transactions/trc20"
                            f"?only_confirmed=true&limit=5&contract_address={USDT_CONTRACT}"
                        )
                        resp = requests.get(url, headers=HEADERS, timeout=10)
                        data = resp.json()

                        if "data" not in data:
                            continue

                        for tx in data["data"]:
                            if tx["to"].lower() != watch.address.lower():
                                continue
                            tx_hash = tx["transaction_id"]
                            if RechargeLog.objects.filter(tx_hash=tx_hash).exists():
                                continue

                            amount = Decimal(tx["value"]) / Decimal(10**6)
                            from_address = tx["from"]
                            to_address = tx["to"]
                            timestamp = int(tx["block_timestamp"]) // 1000
                            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

                            # 写入日志
                            RechargeLog.objects.create(
                                wallet=None,
                                tx_hash=tx_hash,
                                amount=amount,
                                confirmed=True,
                                chain_type="TRC20",
                                token_type="USDT",
                            )

                            # 推送
                            message = (
                                "✅收入USDT 通知\n"
                                f"交易时间 : {dt}\n"
                                f"收入金额 : {amount} USDT\n"
                                f"付款地址 : {from_address}\n"
                                f"收款地址 : {to_address}\n"
                                f"交易哈希 : {tx_hash}"
                            )
                            send_tg_message(watch.chat_id, message)

                    except Exception as e:
                        self.stdout.write(f"❌ 地址 {watch.address} 监听失败: {str(e)}")

                time.sleep(20)

            except KeyboardInterrupt:
                self.stdout.write("🛑 监听已终止")
                break