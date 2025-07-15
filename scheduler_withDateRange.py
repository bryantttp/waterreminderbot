from telethon.sync import TelegramClient
from datetime import datetime, timedelta, time
from dotenv import load_dotenv
import pytz
import os

# Load credentials from .env
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE_NUMBER")
recipient_value = os.getenv("TELEGRAM_ID")

# Define Singapore timezone
sgt = pytz.timezone("Asia/Singapore")

# Initialize Telethon client
client = TelegramClient("session", api_id, api_hash)

async def main():
    await client.start(phone)

    # Get recipient
    recipient = await client.get_entity(recipient_value)

    # Get all currently scheduled messages
    scheduled_msgs = await client.get_messages(recipient, scheduled=True)
    scheduled_datetimes = {
        msg.date.astimezone(sgt).replace(minute=0, second=0, microsecond=0)
        for msg in scheduled_msgs
    }

    # Start from the next full hour
    now = datetime.now(sgt)
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    print("Current time SGT:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"Already scheduled messages found: {len(scheduled_datetimes)}")

    messages_scheduled = len(scheduled_datetimes)
    scheduled_time = next_hour

    while messages_scheduled < 100:
        hour = scheduled_time.hour

        # Skip hours from 3AM to 8AM
        if 3 <= hour <= 8:
            scheduled_time += timedelta(hours=1)
            continue

        # Round to hour and check if already scheduled
        if scheduled_time in scheduled_datetimes:
            print(f"[Skipped] Already scheduled at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} SGT")
        else:
            # Time-based message logic
            if hour == 9:
                message = "Drink up Baby! Please have your breakfast and take your daily supplements (Tribiotix, Yeast B Complex and Vitamin D3) as well!"
            elif hour == 12:
                message = "Drink up Baby! Please have your lunch as well!"
            elif hour == 16:
                message = "Drink up Baby! Please have your snack as well!"
            elif hour == 19:
                message = "Drink up Baby! Please have your dinner as well!"
            else:
                message = "Drink Up Baby!"

            print(f"Scheduling message at: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} SGT")
            await client.send_message(recipient, message=message, schedule=scheduled_time)
            messages_scheduled += 1

        # Move to the next hour
        scheduled_time += timedelta(hours=1)

with client:
    client.loop.run_until_complete(main())
