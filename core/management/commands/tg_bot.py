import os
import sys
import asyncio
import nest_asyncio
from datetime import datetime
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from asgiref.sync import sync_to_async
from core.models import TelegramWatchAddress
from core.utils.wallet import (
    get_trx_balance,
    get_usdt_trc20_balance,
    get_eth_balance,
    get_usdt_erc20_balance,
    get_today_trx_stats,
    get_today_usdt_stats,
    get_today_erc_stats,
)

# ⛑ 补丁：支持嵌套事件循环
nest_asyncio.apply()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 欢迎使用监听机器人！\n请输入 /help 查看可用命令。")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 可用命令：\n"
                                    "/start - 启动机器人\n"
                                    "/help - 获取帮助\n"
                                    "/watch <链> <地址> - 添加监听\n"
                                    "/unwatch <地址> - 删除监听\n"
                                    "/list - 查看已监听地址\n"
                                    "/check  - <地址> - 查看单个钱包地址余额\n"
                                    "/balance - 查询所有地址余额")


@sync_to_async
def add_watch(chat_id, chain_type, address):
    obj, created = TelegramWatchAddress.objects.get_or_create(
        chat_id=chat_id,
        address=address,
        chain_type=chain_type.lower()
    )
    return created


async def watch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("❗用法错误：/watch trc20 TXXXX...")
        return

    chain_type, address = context.args
    if chain_type.lower() not in ["erc20", "trc20"]:
        await update.message.reply_text("❗仅支持链类型：erc20 / trc20")
        return

    chat_id = str(update.effective_chat.id)
    created = await add_watch(chat_id, chain_type, address)

    if created:
        await update.message.reply_text(f"✅ 成功添加监听：{chain_type.upper()} - {address}")
    else:
        await update.message.reply_text("⚠️ 该地址已存在监听。")


@sync_to_async
def get_watch_list(chat_id):
    return list(TelegramWatchAddress.objects.filter(chat_id=chat_id))


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    addresses = await get_watch_list(chat_id)

    if not addresses:
        await update.message.reply_text("📭 当前未监听任何地址。")
    else:
        msg = "📌 当前监听地址：\n"
        for addr in addresses:
            msg += f"- {addr.chain_type.upper()} - {addr.address}\n"
        await update.message.reply_text(msg)


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    addresses = await get_watch_list(chat_id)
    now = datetime.now().strftime("%Y-%m-%d")

    if not addresses:
        await update.message.reply_text("📭 当前未监听任何地址。")
        return

    for addr in addresses:
        if addr.chain_type == 'trc20':
            usdt = await sync_to_async(get_usdt_trc20_balance)(addr.address)
            trx = await sync_to_async(get_trx_balance)(addr.address)
            income, outcome = await sync_to_async(get_today_trx_stats)(addr.address)
            net = income - outcome
            msg = f"\n📅 日期: {now}\n\n"
            msg += f"地址: {addr.address}\n\n"
            msg += f"USDT余额: {usdt:.6f} USDT\nTRX余额: {trx:.6f} TRX\n"
            msg += f"\n今日收入: {income:.6f} TRX\n今日支出: {outcome:.6f} TRX\n今日利润: {net:.6f} TRX"
        else:
            usdt = await sync_to_async(get_usdt_erc20_balance)(addr.address)
            eth = await sync_to_async(get_eth_balance)(addr.address)
            stats = await get_today_usdt_stats(addr.address)
            msg = f"\n📅 日期: {now}\n\n"
            msg += f"地址: {addr.address}\n\n"
            msg += f"USDT余额: {usdt:.6f} USDT\nETH余额: {eth:.6f} ETH\n"
            msg += f"\n今日收入: {stats['income']:.6f} USDT\n今日支出: {stats['outcome']:.6f} USDT\n今日利润: {stats['profit']:.6f} USDT"

        await update.message.reply_text(msg)

@sync_to_async
def remove_watch(chat_id, address):
    return TelegramWatchAddress.objects.filter(chat_id=chat_id, address=address).delete()


async def unwatch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗用法错误：/unwatch <地址>")
        return

    chat_id = str(update.effective_chat.id)
    address = context.args[0]

    deleted_count, _ = await remove_watch(chat_id, address)
    if deleted_count > 0:
        await update.message.reply_text(f"🗑️ 成功删除监听地址：{address}")
    else:
        await update.message.reply_text("⚠️ 未找到该地址的监听记录。")

#单独查看某个地址的余额
async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗用法错误：/check <地址>")
        return

    address = context.args[0]
    now = datetime.now().strftime("%Y-%m-%d")

    # 检测是 TRON 还是 Ethereum 地址
    if address.startswith("T"):  # 简单判断 TRON
        usdt = get_usdt_trc20_balance(address)
        trx = get_trx_balance(address)
        income, expense = get_today_trx_stats(address)
        net = income - expense
        msg = f"📅 日期: {now}\n\n"
        msg += f"地址: {address}\n\n"
        msg += f"USDT余额: {usdt:.6f} USDT\nTRX余额: {trx:.6f} TRX\n"
        msg += f"\n今日收入: {income:.6f} TRX\n今日支出: {expense:.6f} TRX\n今日利润: {net:.6f} TRX"
    else:  # Ethereum
        usdt = get_usdt_erc20_balance(address)
        eth = get_eth_balance(address)
        income, expense = get_today_erc_stats(address)
        net = income - expense
        msg = f"📅 日期: {now}\n\n"
        msg += f"地址: {address}\n\n"
        msg += f"USDT余额: {usdt:.6f} USDT\nETH余额: {eth:.6f} ETH\n"
        msg += f"\n今日收入: {income:.6f} USDT\n今日支出: {expense:.6f} USDT\n今日利润: {net:.6f} USDT"

    await update.message.reply_text(msg)


class Command(BaseCommand):
    help = "启动 Telegram Bot"

    def handle(self, *args, **kwargs):
        token = os.getenv("TG_BOT_TOKEN")
        if not token:
            self.stdout.write(self.style.ERROR("❌ TG_BOT_TOKEN 环境变量未设置"))
            return

        self.stdout.write(self.style.SUCCESS(f"✅ 加载 TOKEN: {token[:10]}..."))

        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("watch", watch_command))
        app.add_handler(CommandHandler("list", list_command))
        app.add_handler(CommandHandler("balance", balance_command))
        app.add_handler(CommandHandler("unwatch", unwatch_command))

        #单独查看某个地址的余额
        app.add_handler(CommandHandler("check", check_command))

        self.stdout.write(self.style.SUCCESS("🤖 Telegram Bot 正在运行..."))

        # ✅ 直接运行异步 bot，避免 asyncio.run 冲突
        loop = asyncio.get_event_loop()
        loop.run_until_complete(app.run_polling())