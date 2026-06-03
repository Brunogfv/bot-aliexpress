# Bot AliExpress — Monitor de Promoções

Bot que busca promoções do AliExpress no Promobit e notifica via Telegram.

## Instalação

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Uso

```powershell
python main.py scan              # mostra promoções no terminal
python main.py scan --telegram   # envia via Telegram
```

## GitHub Actions (rodar todo dia)

1. Crie um repositório privado no GitHub
2. Envie o código:
   ```powershell
   git init
   git add .
   git commit -m "init"
   git remote add origin https://github.com/seu-usuario/bot-aliexpress.git
   git push -u origin main
   ```
3. Em **Settings > Secrets and variables > Actions**, adicione:
   - `TELEGRAM_BOT_TOKEN` — token do @BotFather
   - `TELEGRAM_CHAT_ID` — seu ID do @userinfobot

O workflow roda todo dia às 10:00 BRT.

## Estrutura

```
bot-aliexpress/
├── main.py
├── requirements.txt
├── .github/workflows/scan.yml
├── src/
│   ├── scraper.py    # Busca ofertas no Promobit
│   └── notifier.py   # Envia Telegram
```
