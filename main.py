import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.scraper import fetch_aliexpress_deals, format_telegram, format_text
from src.notifier import send_telegram

import os
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def cmd_scan(send_tg: bool = False):
    print("Buscando promoções do AliExpress...\n")
    deals = fetch_aliexpress_deals(max_deals=15)

    if not deals:
        print("Nenhuma promoção encontrada.")
        return

    print(format_text(deals))

    if send_tg:
        msg = format_telegram(deals)
        ok = send_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
        if ok:
            print("\n  Notificação enviada via Telegram!")
        else:
            print("\n  Falha ao enviar Telegram.")


def cmd_help():
    print("""
Uso: python main.py <comando>

COMANDOS:
  scan                Busca promoções do AliExpress
  scan --telegram     Busca e envia via Telegram

EXEMPLOS:
  python main.py scan
  python main.py scan --telegram
""")


def main():
    if len(sys.argv) < 2:
        cmd_help()
        return

    command = sys.argv[1]
    send_tg = "--telegram" in sys.argv

    if command == "scan":
        cmd_scan(send_tg)
    else:
        cmd_help()


if __name__ == "__main__":
    main()
