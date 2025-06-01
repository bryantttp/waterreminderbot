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

# Define Singapore timezone
sgt = pytz.timezone("Asia/Singapore")

# Initialize Telethon client
client = TelegramClient("session", api_id, api_hash)

async def main():
    await client.start(phone)

    # Get the recipient from .env
    recipient_value = os.getenv("TELEGRAM_ID")
    recipient = await client.get_entity(recipient_value)

    # Fetch scheduled messages once
    scheduled_msgs = await client.get_messages(recipient, scheduled=True)

    # Calculate tomorrow's date in SGT
    now_sgt = datetime.now(sgt)
    tomorrow = now_sgt + timedelta(days=1)
    day_after_tomorrow = now_sgt + timedelta(days=2)

    # Schedule messages from 9 AM to 11 PM tomorrow
    for hour in range(9, 24):  # 24 excluded, ends at 11 PM
        scheduled_dt = sgt.localize(datetime.combine(tomorrow.date(), time(hour, 0)))
        scheduled_dt_utc = scheduled_dt.astimezone(pytz.utc)
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

    # Add one final message at 12:00 AM (00:00) the next day
    midnight_dt = sgt.localize(datetime.combine(day_after_tomorrow.date(), time(0, 0)))
    midnight_utc = midnight_dt.astimezone(pytz.utc)

    already_scheduled = any(msg.date == midnight_utc for msg in scheduled_msgs)
    if already_scheduled:
        print(f"[Skipped] Midnight message already scheduled at {midnight_dt}")
    else:
        final_msg = f"Drink Up Baby!"
        print(f"Scheduling final message at: {midnight_dt.strftime('%Y-%m-%d %H:%M:%S')} SGT")
        await client.send_message(recipient, message=final_msg, schedule=midnight_dt)

with client:
    client.loop.run_until_complete(main())
