# core/utils/address_utils.py
from datetime import datetime
from asgiref.sync import sync_to_async
from core.utils.wallet import (
    get_usdt_trc20_balance,
    get_trx_balance,
    get_today_trx_stats,
    get_usdt_erc20_balance,
    get_eth_balance,
    get_today_usdt_stats,
    get_btc_balance,
    get_today_btc_stats,
)

def is_too_many_addresses(addresses: list, threshold: int = 10) -> bool:
    return len(addresses) > threshold

def infer_chain_type(address: str) -> str:
    """
    根据地址前缀判断链类型（TRON、Ethereum、BTC）
    """
    address = address.strip()

    if address.startswith("T"):  # TRON
        return "trc20"
    elif address.startswith("0x"):  # Ethereum
        return "erc20"
    elif address.startswith("1") or address.startswith("3") or address.startswith("bc1"):  # Bitcoin
        return "btc"
    return "unknown"

async def generate_balance_message(addr, now=None):
    if not now:
        now = datetime.now().strftime("%Y-%m-%d")

    if addr.chain_type == 'trc20':
        usdt = await sync_to_async(get_usdt_trc20_balance)(addr.address)
        trx = await sync_to_async(get_trx_balance)(addr.address)
        income, outcome = await sync_to_async(get_today_trx_stats)(addr.address)
        net = income - outcome
        msg = (
            f"\n📅 日期: {now}\n\n地址: {addr.address}\n\n"
            f"USDT余额: {usdt:.6f} USDT\nTRX余额: {trx:.6f} TRX\n"
            f"\n今日收入: {income:.6f} TRX\n今日支出: {outcome:.6f} TRX\n"
            f"今日利润: {net:.6f} TRX"
        )

    elif addr.chain_type == 'erc20':
        usdt = await sync_to_async(get_usdt_erc20_balance)(addr.address)
        eth = await sync_to_async(get_eth_balance)(addr.address)
        stats = await get_today_usdt_stats(addr.address)
        msg = (
            f"\n📅 日期: {now}\n\n地址: {addr.address}\n\n"
            f"USDT余额: {usdt:.6f} USDT\nETH余额: {eth:.6f} ETH\n"
            f"\n今日收入: {stats['income']:.6f} USDT\n今日支出: {stats['outcome']:.6f} USDT\n"
            f"今日利润: {stats['profit']:.6f} USDT"
        )

    elif addr.chain_type == 'btc':
        btc = await sync_to_async(get_btc_balance)(addr.address)
        income, outcome = await sync_to_async(get_today_btc_stats)(addr.address)
        net = income - outcome
        msg = (
            f"\n📅 日期: {now}\n\n地址: {addr.address}\n\n"
            f"BTC余额: {btc:.8f} BTC\n"
            f"\n今日收入: {income:.8f} BTC\n今日支出: {outcome:.8f} BTC\n"
            f"今日利润: {net:.8f} BTC"
        )

    else:
        msg = f"⚠️ 未知链类型：{addr.chain_type}"

    return msg