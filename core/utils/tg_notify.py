import os
import requests

def send_tg_message(chat_id: str, message: str, parse_mode: str = None):
    """
    向 Telegram 推送消息，可指定 parse_mode（Markdown / HTML）
    """
    token = os.getenv("TG_BOT_TOKEN")
    if not token:
        print("❌ TG_BOT_TOKEN 未设置")
        return False

    if not chat_id:
        chat_id = os.getenv("TG_NOTIFY_CHAT_ID")
        if not chat_id:
            print("❌ TG_NOTIFY_CHAT_ID 未设置")
            return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    if parse_mode:
        data["parse_mode"] = parse_mode

    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            print(f"✅ 已推送消息：{message}")
            return True
        else:
            print(f"❌ 推送失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False