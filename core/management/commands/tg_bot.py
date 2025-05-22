import os
import sys
import asyncio
import nest_asyncio
from datetime import datetime
from django.core.management.base import BaseCommand
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
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
    get_btc_balance,
)

from core.bot_handlers import (
    start,
    help_command,
    watch_command,
    unwatch_command,
    list_command,
    balance_command,
    check_command,
    handle_text
)

from dotenv import load_dotenv
load_dotenv()

from core.utils.address_utils import (
    infer_chain_type,
    generate_balance_message,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from core.utils.address_utils import generate_balance_message, is_too_many_addresses

import threading
from django.core.management.base import BaseCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters
)
from core.webserver import start_web

from core.bot_handlers import (
    start, help_command, watch_command, unwatch_command,
    list_command, balance_command, check_command, handle_text
)



nest_asyncio.apply()
USER_STATE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["💼 查询钱包余额"], ["➕ 添加监控钱包"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🤖 欢迎使用监听机器人！\n请输入 /help 查看可用命令。",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 可用命令：\n"
                                    "/start - 启动机器人\n"
                                    "/help - 获取帮助\n"
                                    "/watch <链> <地址> - 添加监听\n"
                                    "/unwatch <地址> - 删除监听\n"
                                    "/list - 查看已监听地址\n"
                                    "/check <地址> - 查看单个钱包地址余额\n"
                                    "/balance - 查询所有地址余额")

@sync_to_async
def add_watch(chat_id, address):
    chain_type = infer_chain_type(address)
    if chain_type == "unknown":
        raise ValueError("不支持的地址类型")
    obj, created = TelegramWatchAddress.objects.get_or_create(
        chat_id=chat_id,
        address=address,
        chain_type=chain_type
    )
    return created

@sync_to_async
def remove_watch(chat_id, address):
    return TelegramWatchAddress.objects.filter(chat_id=chat_id, address=address).delete()

@sync_to_async
def get_watch_list(chat_id):
    return list(TelegramWatchAddress.objects.filter(chat_id=chat_id))

async def watch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗用法错误：/watch <地址>")
        return

    address = context.args[0]
    chain_type = infer_chain_type(address)

    if chain_type == "unknown":
        await update.message.reply_text("❗无法识别地址链类型，请检查地址格式")
        return

    chat_id = str(update.effective_chat.id)
    created, _ = await sync_to_async(TelegramWatchAddress.objects.get_or_create)(
        chat_id=chat_id,
        address=address,
        chain_type=chain_type
    )

    if created:
        await update.message.reply_text(f"✅ 成功添加监听：{chain_type.upper()} - {address}")
    else:
        await update.message.reply_text("⚠️ 地址已存在监听。")

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

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    addresses = await get_watch_list(chat_id)

    if not addresses:
        await update.message.reply_text("📭 当前未监听任何地址。")
        return
    base_url = settings.WEB_DOMAIN
    url = f"{base_url}/watchlist/{chat_id}"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 查看我的监听地址", url=url)]
    ])

    await update.message.reply_text(
        "🔗 请点击下方按钮查看你的监听地址列表：",
        reply_markup=keyboard
    )


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    addresses = await get_watch_list(chat_id)
    now = datetime.now().strftime("%Y-%m-%d")

    if not addresses:
        await update.message.reply_text("📭 当前未监听任何地址。")
        return

    if await is_too_many_addresses(addresses):
        await update.message.reply_text(
            f"⚠️ 当前监听地址数量为 {len(addresses)} 个，超出批量查询上限（最多 10 个）。\n"
            f"👉 请使用 `/check <地址>` 命令单独查询余额。",
            parse_mode="Markdown"
        )
        return

    for addr in addresses:
        msg = await generate_balance_message(addr, now)
        await update.message.reply_text(msg)

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗用法错误：/check <地址>")
        return
    await run_check_logic(update, context.args[0])

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    text = update.message.text.strip()
    if text == "💼 查询钱包余额":
        USER_STATE[chat_id] = "waiting_check_address"
        await update.message.reply_text("📥 请发送你要查询的地址：")
        return
    if text == "➕ 添加监控钱包":
        USER_STATE[chat_id] = "waiting_watch_address"
        await update.message.reply_text("📥 请发送你要添加的地址（支持 ERC20 / TRC20 / BTC）：")
        return
    state = USER_STATE.get(chat_id)
    if state == "waiting_check_address":
        USER_STATE.pop(chat_id, None)
        await run_check_logic(update, text)
        return
    if state == "waiting_watch_address":
        USER_STATE.pop(chat_id, None)
        await run_watch_logic(update, chat_id, text)
        return
    await update.message.reply_text("⚠️ 无法识别地址格式，请点击按钮后发送地址。")

async def run_check_logic(update: Update, address: str):
    try:
        now = datetime.now().strftime("%Y-%m-%d")
        if address.startswith("T"):
            usdt = get_usdt_trc20_balance(address)
            trx = get_trx_balance(address)
            income, outcome = get_today_trx_stats(address)
            net = income - outcome
            msg = f"📅 日期: {now}\n\n地址: {address}\n\nUSDT余额: {usdt:.6f} USDT\nTRX余额: {trx:.6f} TRX\n"
            msg += f"\n今日收入: {income:.6f} TRX\n今日支出: {outcome:.6f} TRX\n今日利润: {net:.6f} TRX"
        elif address.startswith("0x"):
            usdt = get_usdt_erc20_balance(address)
            eth = get_eth_balance(address)
            income, outcome = get_today_erc_stats(address)
            net = income - outcome
            msg = f"📅 日期: {now}\n\n地址: {address}\n\nUSDT余额: {usdt:.6f} USDT\nETH余额: {eth:.6f} ETH\n"
            msg += f"\n今日收入: {income:.6f} USDT\n今日支出: {outcome:.6f} USDT\n今日利润: {net:.6f} USDT"
        elif address.startswith(("1", "3", "bc1")):
            btc = get_btc_balance(address)
            msg = f"📅 日期: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            msg += f"地址: {address}\n\n"
            msg += f"BTC余额: {btc:.8f} BTC"
        else:
            msg = f"⚠️ 无法识别地址格式：{address}"
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ 查询失败: {e}")

async def run_watch_logic(update: Update, chat_id: str, address: str):
    try:
        chain_type = infer_chain_type(address)
        if chain_type == "unknown":
            await update.message.reply_text("❗无法识别地址链类型，请检查地址格式")
            return

        created, _ = await sync_to_async(TelegramWatchAddress.objects.get_or_create)(
            chat_id=chat_id,
            address=address,
            chain_type=chain_type
        )
        if created:
            await update.message.reply_text(f"✅ 成功添加监听：{chain_type.upper()} - {address}")
        else:
            await update.message.reply_text("⚠️ 地址已存在监听。")
    except Exception as e:
        await update.message.reply_text(f"❌ 添加失败: {e}")


class Command(BaseCommand):
    help = "启动 Telegram Bot"

    def handle(self, *args, **kwargs):
        token = os.getenv("TG_BOT_TOKEN")
        if not token:
            self.stdout.write(self.style.ERROR("❌ TG_BOT_TOKEN 环境变量未设置"))
            return

        self.stdout.write(self.style.SUCCESS(f"✅ 加载 TOKEN: {token[:10]}..."))

        # ✅ 启动 Web 服务线程
        web_thread = threading.Thread(target=start_web, daemon=True)
        web_thread.start()
        self.stdout.write(self.style.SUCCESS("🌐 Web 服务已启动"))

        # ✅ 初始化 Telegram Bot
        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("watch", watch_command))
        app.add_handler(CommandHandler("unwatch", unwatch_command))
        app.add_handler(CommandHandler("list", list_command))
        app.add_handler(CommandHandler("balance", balance_command))
        app.add_handler(CommandHandler("check", check_command))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

        self.stdout.write(self.style.SUCCESS("🤖 Telegram Bot 正在运行..."))

        # ✅ 启动 Bot 的事件循环（阻塞）
        loop = asyncio.get_event_loop()
        loop.run_until_complete(app.run_polling())