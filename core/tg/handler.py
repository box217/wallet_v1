import os
import telebot
from core.models import TelegramWatchAddress
from django.db import IntegrityError
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# 用户当前添加监听的链类型缓存（chat_id => chain_type）
USER_CHAIN_TYPE = {}
USER_DELETE_STATE = {}  # 用于存储等待删除序号的 chat_id

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "👋 欢迎使用监听机器人，使用 /watch 添加地址，/list 查看监听地址，/help 查看所有指令。")

@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.reply_to(message, (
        "🛠 支持的指令：\n"
        "/watch - 添加监听地址\n"
        "/list - 查看已监听地址\n"
        "/help - 查看帮助信息"
    ))

@bot.message_handler(commands=["watch"])
def handle_watch(message):
    chat_id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("ERC20", "TRC20")
    bot.send_message(chat_id, "🔗 请选择链类型：", reply_markup=markup)

    USER_CHAIN_TYPE[chat_id] = None  # 等待用户选择链类型

@bot.message_handler(commands=["list"])
def handle_list(message):
    chat_id = str(message.chat.id)
    watches = TelegramWatchAddress.objects.filter(chat_id=chat_id)
    if not watches.exists():
        bot.send_message(chat_id, "📭 当前未监听任何地址")
    else:
        lines = [f"✅ {w.chain_type.upper()} - {w.address}" for w in watches]
        bot.send_message(chat_id, "\n".join(lines))

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # 用户刚选择链类型
    if text.upper() in ("ERC20", "TRC20"):
        USER_CHAIN_TYPE[chat_id] = text.lower()
        bot.send_message(chat_id, f"📥 请发送你要监听的 {text} 地址：")
        return

    # 用户正在添加钱包地址
    if chat_id in USER_CHAIN_TYPE and USER_CHAIN_TYPE[chat_id]:
        chain_type = USER_CHAIN_TYPE.pop(chat_id)
        address = text

        try:
            TelegramWatchAddress.objects.create(
                chat_id=str(chat_id),
                address=address,
                chain_type=chain_type
            )
            bot.send_message(chat_id, f"✅ 地址已绑定成功，监听 {chain_type.upper()}：\n`{address}`", parse_mode="Markdown")
        except IntegrityError:
            bot.send_message(chat_id, f"⚠️ 地址已存在监听记录：{address}")
        return
        # 检查是否在等待用户输入要删除的序号
    if str(chat_id) in USER_DELETE_STATE:
        try:
            idx = int(text.strip())
            address_ids = USER_DELETE_STATE.pop(str(chat_id))
            if 1 <= idx <= len(address_ids):
                addr_id = address_ids[idx - 1]
                TelegramWatchAddress.objects.filter(id=addr_id).delete()
                bot.send_message(chat_id, "✅ 地址已删除")
            else:
                bot.send_message(chat_id, "❌ 编号超出范围，请重新使用 /delete 操作")
        except ValueError:
            bot.send_message(chat_id, "❌ 输入无效，请输入数字编号")
        return

    # 如果非链选择阶段的纯文本
    bot.send_message(chat_id, "🤖 指令未识别。请使用 /watch 添加钱包地址，或 /help 查看帮助。")

    @bot.message_handler(commands=["delete"])
    def handle_delete(message):
        chat_id = str(message.chat.id)
        watches = TelegramWatchAddress.objects.filter(chat_id=chat_id)
        if not watches.exists():
            bot.send_message(chat_id, "📭 当前未监听任何地址")
            return

        msg_lines = ["🗑 请输入你要删除的地址编号："]
        for idx, w in enumerate(watches, start=1):
            msg_lines.append(f"{idx}. {w.chain_type.upper()} - {w.address}")

        USER_DELETE_STATE[chat_id] = list(watches.values_list("id", flat=True))
        bot.send_message(chat_id, "\n".join(msg_lines))