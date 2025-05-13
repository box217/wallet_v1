import time
import os
from decimal import Decimal
from django.core.management.base import BaseCommand
from web3 import Web3

from core.models import TelegramWatchAddress, RechargeLog
from core.utils.tg_notify import send_tg_message

# Geth POA middleware shim
def geth_poa_middleware(make_request, web3):
    def middleware(method, params):
        if method in ('eth_getBlockByHash', 'eth_getBlockByNumber'):
            block = make_request(method, params)
            if block and 'result' in block and block['result']:
                block['result']['populate'] = lambda: None
        return make_request(method, params)
    return middleware

class Command(BaseCommand):
    help = "监听所有ERC20 USDT代币收入"

    def handle(self, *args, **options):
        self.stdout.write("🚀 正在监听 ERC20 USDT 地址收入...")

        w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
        if not w3.is_connected():
            self.stdout.write("❌ 无法连接到以太坊节点")
            return

        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        USDT_CONTRACT = Web3.to_checksum_address("0xdAC17F958D2ee523a2206206994597C13D831ec7")
        TRANSFER_TOPIC = w3.keccak(text="Transfer(address,address,uint256)").hex()

        last_block = w3.eth.block_number - 5

        while True:
            try:
                current_block = w3.eth.block_number
                watches = TelegramWatchAddress.objects.filter(chain_type="erc20")

                for watch in watches:
                    try:
                        to_address = Web3.to_checksum_address(watch.address)
                        logs = w3.eth.get_logs({
                            "fromBlock": last_block,
                            "toBlock": current_block,
                            "address": USDT_CONTRACT,
                            "topics": [
                                TRANSFER_TOPIC,
                                None,
                                f"0x{'0'*24}{to_address[2:].lower()}"
                            ]
                        })

                        for log in logs:
                            tx_hash = log['transactionHash'].hex()
                            if RechargeLog.objects.filter(tx_hash=tx_hash).exists():
                                continue

                            value = int(log['data'], 16) / 1_000_000

                            tx = w3.eth.get_transaction(log['transactionHash'])
                            from_address = tx['from']

                            message = (
                                f"✅收入USDT 通知\n"
                                f"交易时间 : 待查询\n"
                                f"收入金额 : {value} USDT\n"
                                f"付款地址 : {from_address}\n"
                                f"收款地址 : {to_address}\n"
                                f"交易哈希 : {tx_hash}"
                            )
                            send_tg_message(watch.chat_id, message)

                            RechargeLog.objects.create(
                                tx_hash=tx_hash,
                                amount=value,
                                confirmed=True,
                                chain_type="ERC20",
                                token_type="USDT"
                            )

                            self.stdout.write(f"✅ 已推送消息：{tx_hash}")

                    except Exception as e:
                        self.stdout.write(f"⚠️ 地址 {watch.address} 监听异常: {e}")

                last_block = current_block + 1
                time.sleep(30)

            except Exception as e:
                self.stdout.write(f"⚠️ 主循环异常: {e}")
                time.sleep(60)