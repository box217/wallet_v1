import os
import time
from decimal import Decimal
from django.core.management.base import BaseCommand
from web3 import Web3
from core.models import TelegramWatchAddress, RechargeLog
from core.utils.tg_notify import send_tg_message
from core.utils.wallet import get_eth_balance, get_token_balance, get_today_erc_stats

TOKENS = {
    "USDT": {
        "contract": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "decimals": 6,
    },
    "USDC": {
        "contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "decimals": 6,
    }
}

def to_checksum(address):
    return Web3.to_checksum_address(address)

def get_topic(w3):
    return w3.keccak(text="Transfer(address,address,uint256)").hex()

class Command(BaseCommand):
    help = "监听所有 ERC20 收入与支出"

    def handle(self, *args, **options):
        self.stdout.write("🚀 正在监听 ERC20 地址...")

        w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
        if not w3.is_connected():
            self.stdout.write("❌ 无法连接 Ethereum")
            return

        TRANSFER_TOPIC = get_topic(w3)
        last_block = w3.eth.block_number - 5

        while True:
            try:
                current_block = w3.eth.block_number
                watches = TelegramWatchAddress.objects.filter(chain_type="erc20")

                for token_name, token_info in TOKENS.items():
                    token_addr = to_checksum(token_info["contract"])
                    decimals = token_info["decimals"]

                    for watch in watches:
                        try:
                            addr = to_checksum(watch.address)
                            # 监听收入和支出
                            logs = w3.eth.get_logs({
                                "fromBlock": last_block,
                                "toBlock": current_block,
                                "address": token_addr,
                                "topics": [TRANSFER_TOPIC, None, None],
                            })

                            for log in logs:
                                topics = log["topics"]
                                from_addr = "0x" + topics[1].hex()[-40:]
                                to_addr = "0x" + topics[2].hex()[-40:]
                                from_addr = to_checksum(from_addr)
                                to_addr = to_checksum(to_addr)

                                # 收入或支出和当前地址有关
                                if addr not in (from_addr, to_addr):
                                    continue

                                tx_hash = log["transactionHash"].hex()
                                if RechargeLog.objects.filter(tx_hash=tx_hash).exists():
                                    continue

                                value = int(log["data"], 16) / (10 ** decimals)
                                tx = w3.eth.get_transaction(log["transactionHash"])
                                dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(w3.eth.get_block(log["blockNumber"])["timestamp"]))

                                is_income = to_addr == addr
                                symbol = f"+{value}" if is_income else f"-{value}"
                                emoji = "\U0001F7E2" if is_income else "\U0001F534"
                                title = f"{'收入' if is_income else '支出'}{token_name}"

                                eth_bal = get_eth_balance(watch.address)
                                token_bal = get_token_balance(watch.address, token_name)
                                stats = get_today_erc_stats(watch.address)

                                msg = (
                                    f"{emoji}{title} 提醒       {symbol} {token_name}\n\n"
                                    f"地址备注: \n\n"
                                    f"付款地址: {from_addr}\n"
                                    f"收款地址: {to_addr}\n"
                                    f"交易时间:    {dt}\n"
                                )
                                if is_income:
                                    msg += f"交易金额:    +{value} {token_name}\n"

                                msg += (
                                    f"{token_name}余额:  {token_bal:.6f} {token_name}\n"
                                    f"ETH余额:   {eth_bal:.6f} ETH\n\n"
                                    f"今日收入: {stats[0]} {token_name}\n"
                                    f"今日支出: {stats[1]} {token_name}\n"
                                    f"今日利润: {stats[0] - stats[1]} {token_name}\n\n"
                                    f"[🔍查看交易详情](https://etherscan.io/tx/{tx_hash})"
                                )

                                send_tg_message(watch.chat_id, msg, parse_mode="Markdown")

                                RechargeLog.objects.create(
                                    tx_hash=tx_hash,
                                    amount=Decimal(value),
                                    confirmed=True,
                                    chain_type="ERC20",
                                    token_type=token_name,
                                )

                        except Exception as e:
                            self.stdout.write(f"⚠️ 地址 {watch.address} 监听异常: {e}")

                last_block = current_block + 1
                time.sleep(90)

            except Exception as e:
                self.stdout.write(f"⚠️ 主循环异常: {e}")
                time.sleep(90)

