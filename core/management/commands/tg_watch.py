from django.core.management.base import BaseCommand
from core.tg.handler import bot

class Command(BaseCommand):
    help = "启动 Telegram 钱包监听机器人"

    def handle(self, *args, **options):
        print("🤖 Telegram Bot 正在运行...")
        bot.infinity_polling()