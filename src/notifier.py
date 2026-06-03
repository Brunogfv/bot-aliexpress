import urllib.request
import urllib.parse
import json
import ssl
import os


def send_telegram(token: str, chat_id: str, message: str) -> bool:
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("  Telegram não configurado. Defina TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }).encode()

    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, data=data)
        resp = urllib.request.urlopen(req, context=ctx, timeout=15)
        result = json.loads(resp.read())
        return result.get("ok", False)
    except Exception as e:
        print(f"  Erro ao enviar Telegram: {e}")
        return False
