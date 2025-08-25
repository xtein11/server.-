# server.-import os, json, requests
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID        = os.getenv("TELEGRAM_CHAT_ID", "")
ALERT_SECRET   = os.getenv("ALERT_SECRET", "CHANGE_ME")

def send_telegram(text: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{7960236842:AAHh8VL9Q9cUVa_H1rlDqWHRtoDE2iCsC2Q}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    if secret != ALERT_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    raw = await request.body()
    text = raw.decode("utf-8", errors="ignore").strip()
    # Попробуем распарсить JSON; если нет — отправим как есть
    try:
        payload = await request.json()
        text = f"🔔 TV Alert\n{json.dumps(payload, ensure_ascii=False, indent=2)}"
    except Exception:
        # text уже содержит тело как строку
        text = f"🔔 TV Alert (text)\n{text}"
    send_telegram(text)
    return {"ok": True}

@app.get("/")
def health():
    return {"status": "ok"}
