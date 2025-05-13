import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from core.models import TelegramWatchAddress
import django
import sys

# 初始化 Django 环境
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet_backend.settings")
django.setup()

# 读取 Bot Token
token = os.getenv("TG_BOT_TOKEN")

# 设置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# /start 和 /help 指令
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/add <地址> <链类型: erc20/trc20>\n/list\n/remove <地址>\n/help"
    )

# /add <地址> <链类型>
async def add_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("用法: /add <地址> <erc20|trc20>")
        return

    address, chain = context.args
    chat_id = str(update.effective_chat.id)

    if chain.lower() not in ('erc20', 'trc20'):
        await update.message.reply_text("链类型只能是 erc20 或 trc20")
        return

    obj, created = TelegramWatchAddress.objects.get_or_create(
        chat_id=chat_id,
        address=address,
        chain_type=chain.lower()
    )

    if created:
        await update.message.reply_text(f"✅ 已绑定: {address} ({chain})")
    else:
        await update.message.reply_text("该地址已存在绑定记录")

# /list
async def list_addresses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    qs = TelegramWatchAddress.objects.filter(chat_id=chat_id)

    if not qs.exists():
        await update.message.reply_text("暂无绑定地址")
        return

    lines = [f"{x.address} ({x.chain_type})" for x in qs]
    await update.message.reply_text("\n".join(lines))

# /remove <地址>
async def remove_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("用法: /remove <地址>")
        return

    chat_id = str(update.effective_chat.id)
    count, _ = TelegramWatchAddress.objects.filter(chat_id=chat_id, address=context.args[0]).delete()
    if count:
        await update.message.reply_text("✅ 删除成功")
    else:
        await update.message.reply_text("未找到绑定记录")

# 启动函数
def main():
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", help_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add_address))
    app.add_handler(CommandHandler("list", list_addresses))
    app.add_handler(CommandHandler("remove", remove_address))

    app.run_polling()

if __name__ == "__main__":
    main()