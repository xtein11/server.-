import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ALERT_SECRET = os.getenv("ALERT_SECRET")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@app.get("/")
def home():
    return {"status": "ok", "message": "Bot is running!"}


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()

        # если TradingView шлёт секрет
        secret = data.get("secret")
        if ALERT_SECRET and secret != ALERT_SECRET:
            return {"ok": False, "error": "Invalid secret"}

        # сообщение в телегу
        text = f"🚀 Новый сигнал от TradingView:\n{data}"
        payload = {"chat_id": CHAT_ID, "text": text}
        requests.post(TELEGRAM_URL, data=payload)

        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
