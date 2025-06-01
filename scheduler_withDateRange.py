from telethon.sync import TelegramClient
from datetime import datetime, timedelta, date, time
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

# Set date range (inclusive)
start_date = date(2025, 6, 5)
end_date = date(2025, 6, 6)

# Initialize Telethon client
client = TelegramClient("session", api_id, api_hash)

async def main():
    await client.start(phone)

    # Get recipient from .env
    recipient = await client.get_entity(recipient_value)

    # Fetch scheduled messages once
    scheduled_msgs = await client.get_messages(recipient, scheduled=True)

    current_date = start_date
    while current_date <= end_date:
        for hour in range(9, 24):  # 9 AM to 11 PM
            scheduled_dt = sgt.localize(datetime.combine(current_date, time(hour, 0)))
            scheduled_dt_utc = scheduled_dt.astimezone(pytz.utc)
            # Avoid duplicate scheduled messages
            already_scheduled = any(msg.date == scheduled_dt_utc for msg in scheduled_msgs)
            if already_scheduled:
                print(f"[Skipped] Already scheduled at {scheduled_dt}")
            else:
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
                print(f"Scheduling message at: {scheduled_dt.strftime('%Y-%m-%d %H:%M:%S')} SGT")
                await client.send_message(recipient, message=message, schedule=scheduled_dt)

        # Schedule 12:00 AM for next day (midnight)
        midnight_dt = sgt.localize(datetime.combine(current_date + timedelta(days=1), time(0, 0)))
        midnight_utc = midnight_dt.astimezone(pytz.utc)

        already_scheduled = any(msg.date == midnight_utc for msg in scheduled_msgs)
        if already_scheduled:
            print(f"[Skipped] Midnight message already scheduled at {midnight_dt}")
        else:
            midnight_msg = f"Drink Up Baby!"
            print(f"Scheduling midnight message at: {midnight_dt}")
            await client.send_message(recipient, message=midnight_msg, schedule=midnight_dt)

        current_date += timedelta(days=1)

with client:
    client.loop.run_until_complete(main())
