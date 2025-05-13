from django.core.management.base import BaseCommand
from core.models import WalletAddress, RechargeLog, MerchantCollectionAddress, CollectionLog
from django.utils import timezone
import random, string, requests, os
from decimal import Decimal
from core.utils.crypto import decrypt_private_key
from core.chain.eth import transfer_eth, transfer_token
from core.utils.telegram import send_tg_message

MOCK_TX_HASHES = set()

def random_tx_hash():
    while True:
        tx = '0x' + ''.join(random.choices('abcdef' + string.digits, k=64))
        if tx not in MOCK_TX_HASHES:
            MOCK_TX_HASHES.add(tx)
            return tx

def simulate_incoming_transaction(wallet):
    amount = round(random.uniform(1, 500), 6)
    tx_hash = random_tx_hash()
    print(f"[模拟到账] 地址: {wallet.address}, 币种: {wallet.token_type}, 金额: {amount}, 回调Hash: {tx_hash}")

    RechargeLog.objects.create(
        wallet=wallet,
        tx_hash=tx_hash,
        amount=amount,
        confirmed=True,
        chain_type=wallet.chain_type,
        token_type=wallet.token_type,
    )

    user = wallet.user
    merchant = user.merchant
    callback_url = merchant.callback_url

    payload = {
        "merchant_key": merchant.api_key,
        "user_id": user.user_id,
        "chain": wallet.chain_type,
        "token": wallet.token_type,
        "amount": str(amount),
        "tx_hash": tx_hash,
        "address": wallet.address,
    }

    try:
        resp = requests.post(callback_url, json=payload, timeout=5)
        print(f"[通知成功] {callback_url} -> 状态码: {resp.status_code}")
    except Exception as e:
        print(f"[通知失败] {e}")

    # ===== 自动归集 (真实链转账) =====
    try:
        coll = MerchantCollectionAddress.objects.get(
            merchant=merchant,
            chain_type=wallet.chain_type,
            token_type=wallet.token_type,
            enabled=True
        )
        print(f"[准备归集] 将 {amount} {wallet.token_type} 转入: {coll.collection_address}")

        # 解密私钥
        secret_key = os.getenv("WALLET_SECRET_KEY", "")
        private_key = decrypt_private_key(wallet.encrypted_private_key, secret_key)

        # 执行转账
        if wallet.token_type.lower() == "eth":
            tx_hash2 = transfer_eth(private_key, coll.collection_address, Decimal(amount))
        else:
            TOKEN_CONTRACTS = {
                "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eb48"
            }
            token_contract = TOKEN_CONTRACTS.get(wallet.token_type.lower())
            if not token_contract:
                print(f"[错误] 不支持的币种: {wallet.token_type}")
                return
            tx_hash2 = transfer_token(token_contract, private_key, coll.collection_address, Decimal(amount))

        print(f"[归集成功] tx: {tx_hash2}")

        CollectionLog.objects.create(
            wallet=wallet,
            to_address=coll.collection_address,
            amount=amount,
            tx_hash=tx_hash2,
            chain_type=wallet.chain_type,
            token_type=wallet.token_type,
            success=True
        )

    except MerchantCollectionAddress.DoesNotExist:
        print(f"[警告] 未找到可用的归集地址")
    except Exception as e:
        print(f"[归集失败] {e}")

    # ===== Telegram 通知 =====
    send_tg_message(
        chat_id=None,
        message=f"📥 收到充值：\n币种: {wallet.token_type.upper()} ({wallet.chain_type.upper()})\n金额: {amount}\n地址: `{wallet.address}`"
    )

class Command(BaseCommand):
    help = "模拟到账、通知平台、执行归集并记录归集日志，并发送 TG 通知"

    def handle(self, *args, **options):
        wallets = WalletAddress.objects.all().order_by('?')[:5]
        for wallet in wallets:
            simulate_incoming_transaction(wallet)
