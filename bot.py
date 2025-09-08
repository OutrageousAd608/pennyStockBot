import os
import praw
import requests
from flask import Flask
import threading

# ---- Reddit & Telegram setup ----
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

subreddit = reddit.subreddit("pennystocks")

# ---- Telegram Bot Function ----
def run_bot():
    # send test message on startup
    requests.post(URL, data={"chat_id": CHAT_ID, "text": "✅ Bot is running on Render!"})

    for submission in subreddit.stream.submissions(skip_existing=True):
        message = f"🚨 New Post in r/pennystocks 🚨\n\n{submission.title}\n{submission.url}"
        try:
            requests.post(URL, data={"chat_id": CHAT_ID, "text": message})
            print(f"Sent: {submission.title}")
        except Exception as e:
            print(f"Error sending message: {e}")

# ---- Start bot in background thread ----
threading.Thread(target=run_bot, daemon=True).start()

# ---- Minimal web server for Render ----
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
