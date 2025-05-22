import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
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
    get_today_btc_stats
)
from core.utils.address_utils import (
    infer_chain_type,
    generate_balance_message,
    is_too_many_addresses
)

USER_STATE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["\U0001F4BC 查询钱包余额"], ["\u2795 添加监控钱包"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🤖 欢迎使用监听机器人！\n请输入 /help 查看可用命令。", reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 可用命令：\n"
                                    "/start - 启动机器人\n"
                                    "/help - 获取帮助\n"
                                    "/watch <地址> - 添加监听\n"
                                    "/unwatch <地址> - 删除监听\n"
                                    "/list - 查看已监听地址\n"
                                    "/check <地址> - 查看单个钱包地址余额\n"
                                    "/balance - 查询所有地址余额")

@sync_to_async
def get_watch_list(chat_id):
    return list(TelegramWatchAddress.objects.filter(chat_id=chat_id))

@sync_to_async
def add_watch(chat_id, address):
    chain_type = infer_chain_type(address)
    if chain_type == "unknown":
        return None, False
    return TelegramWatchAddress.objects.get_or_create(chat_id=chat_id, address=address, chain_type=chain_type)

@sync_to_async
def remove_watch(chat_id, address):
    return TelegramWatchAddress.objects.filter(chat_id=chat_id, address=address).delete()

async def watch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❗用法错误：/watch <地址>")
        return

    address = context.args[0]
    chat_id = str(update.effective_chat.id)
    created_obj = await add_watch(chat_id, address)

    if created_obj is None:
        await update.message.reply_text("❗无法识别地址类型，请确认是 TRC20 / ERC20 / BTC 地址")
        return

    created = created_obj[1]
    if created:
        await update.message.reply_text(f"✅ 成功添加监听：{address}")
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

    domain = os.getenv("PUBLIC_DOMAIN", "https://example.com")
    url = f"{domain}/watchlist/{chat_id}"

    button = [[InlineKeyboardButton("点击查看监听列表", url=url)]]
    reply_markup = InlineKeyboardMarkup(button)

    await update.message.reply_text("📬 请点击下方按钮查看你的监听地址：", reply_markup=reply_markup)

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    addresses = await get_watch_list(chat_id)
    now = datetime.now().strftime("%Y-%m-%d")

    if not addresses:
        await update.message.reply_text("📭 当前未监听任何地址。")
        return

    if is_too_many_addresses(addresses):
        await update.message.reply_text("⚠️ 地址数量过多，请使用 /check <地址> 单独查询")
        return

    for addr in addresses:
        msg = await generate_balance_message(addr, now=now)
        await update.message.reply_text(msg)

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗用法错误：/check <地址>")
        return

    address = context.args[0]
    dummy = TelegramWatchAddress(address=address, chain_type=infer_chain_type(address))
    msg = await generate_balance_message(dummy)
    await update.message.reply_text(msg)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    text = update.message.text.strip()

    if text == "\U0001F4BC 查询钱包余额":
        USER_STATE[chat_id] = "waiting_check_address"
        await update.message.reply_text("\U0001F4E5 请发送你要查询的地址：")
        return

    if text == "\u2795 添加监控钱包":
        USER_STATE[chat_id] = "waiting_watch_address"
        await update.message.reply_text("\U0001F4E5 请发送你要添加的地址（支持 ERC20 / TRC20 / BTC）：")
        return

    state = USER_STATE.get(chat_id)
    if state == "waiting_check_address":
        USER_STATE.pop(chat_id, None)
        dummy = TelegramWatchAddress(address=text, chain_type=infer_chain_type(text))
        msg = await generate_balance_message(dummy)
        await update.message.reply_text(msg)
        return

    if state == "waiting_watch_address":
        USER_STATE.pop(chat_id, None)
        created_obj = await add_watch(chat_id, text)
        if created_obj is None:
            await update.message.reply_text("❗无法识别地址类型。")
        elif created_obj[1]:
            await update.message.reply_text(f"✅ 成功添加监听：{text}")
        else:
            await update.message.reply_text("⚠️ 地址已存在监听。")
        return

    await update.message.reply_text("⚠️ 无法识别地址格式，请点击按钮后发送地址。")