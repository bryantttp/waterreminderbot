from telethon.sync import TelegramClient
from datetime import datetime, timedelta, time
from dotenv import load_dotenv
import pytz
import os

# Load credentials from .env file
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE_NUMBER")

# Define timezone for Singapore (UTC+8)
sgt = pytz.timezone("Asia/Singapore")

# Initialize client session
client = TelegramClient("session", api_id, api_hash)

async def main():
    await client.start(phone)

    # Get the recipient from .env
    recipient_value = os.getenv("TELEGRAM_ID")
    recipient = await client.get_entity(recipient_value)

    # Get current time in Singapore
    now = datetime.now(sgt)
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    # Schedule messages from the next hour to 11 PM
    for hour in range(next_hour.hour, 24):  # up to 11 PM
        scheduled_time = sgt.localize(datetime.combine(now.date(), time(hour, 0)))
        if scheduled_time < now:
            scheduled_time += timedelta(days=1)
        if hour == 9:
            message = f"Drink up Baby! Please have your breakfast as well!"
        elif hour == 12:
            message = f"Drink up Baby! Please have your lunch as well!"
        elif hour == 16:
            message = f"Drink up Baby! Please have your snack as well!"
        elif hour == 19:
            message = f"Drink up Baby! Please have your dinner as well!"
        else:
            message = f"Drink Up Baby!"
        print(f"Scheduling message at: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} SGT")
        await client.send_message(recipient, message=message, schedule=scheduled_time)

    # Schedule final message at 12:00 AM (midnight of the next day)
    midnight = sgt.localize(datetime.combine(now.date() + timedelta(days=1), time(0, 0)))
    final_message = "Drink Up Baby!"
    print(f"Scheduling final message at: {midnight.strftime('%Y-%m-%d %H:%M:%S')} SGT")
    await client.send_message(recipient, message=final_message, schedule=midnight)

with client:
    client.loop.run_until_complete(main())
