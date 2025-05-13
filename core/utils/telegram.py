def send_tg_message(chat_id: str, message: str) -> bool:
    """
    发送 Telegram 消息到指定 chat_id
    """
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = chat_id or os.getenv("TG_NOTIFY_CHAT_ID")

    if not token or not chat_id:
        print("[错误] 缺少 TG_BOT_TOKEN 或 TG_NOTIFY_CHAT_ID")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()
        print(f"[TG] ✅ 消息已发送: {message}")
        return True
    except requests.RequestException as e:
        print(f"[TG] ❌ 发送失败: {e}")
        return False