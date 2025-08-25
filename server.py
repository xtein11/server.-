from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # токен бота из переменных окружения
# CHAT_ID можно не указывать, т.к. берём chat_id из апдейта

@app.route('/')
def home():
    return "✅ Bot is running on Render!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Update from Telegram:", data, flush=True)  # выводим апдейты в логи Render

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # --- Логика автоответа ---
        if text.lower() in ["привет", "hi", "hello"]:
            reply = "👋 Привет! Я твой сигнальный бот."
        else:
            reply = f"Ты написал: {text}"

        # Отправляем ответ в Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": reply}
        requests.post(url, json=payload)

    return "ok", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
