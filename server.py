from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "7960236842:AAHh8VL9Q9cUVa_H1rlDqWHRtoDE2iCsC2Q"
CHAT_ID = "-1002959148032"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    message = data.get("message") or str(data)

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
