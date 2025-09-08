import os
import praw
import requests

# ---- Load credentials from environment variables ----
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

subreddit = reddit.subreddit("pennystocks")

# Test message on startup
requests.post(URL, data={"chat_id": CHAT_ID, "text": "✅ Bot is now running on Render!"})

for submission in subreddit.stream.submissions(skip_existing=True):
    message = f"🚨 New Post in r/pennystocks 🚨\n\n{submission.title}\n{submission.url}"
    requests.post(URL, data={"chat_id": CHAT_ID, "text": message})
    print(f"Sent: {submission.title}")
