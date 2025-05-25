import time
import schedule
import os
from telegram import Bot

# Get from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def send_reminder():
    bot.send_message(chat_id=CHAT_ID, text="💧 Time to drink water!")

# Schedule messages every hour from 12PM to 12AM
for hour in range(12, 24):
    schedule.every().day.at(f"{hour:02}:00").do(send_reminder)

print("Bot is running...")

while True:
    schedule.run_pending()
    time.sleep(300)
