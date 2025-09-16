from telethon.sync import TelegramClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz
import os

# Load credentials from .env
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE_NUMBER")
recipient_value = os.getenv("TELEGRAM_ID")

# Define timezone
sgt = pytz.timezone("Asia/Singapore")
log_file = "scheduled_times.log"

# Initialize client
client = TelegramClient("session", api_id, api_hash)

# Load log of previously scheduled times
def load_logged_times():
    if not os.path.exists(log_file):
        return set()
    with open(log_file, "r") as f:
        return {
            datetime.strptime(line.strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=sgt)
            for line in f.readlines()
        }

# Save a new time to the log
def append_logged_time(dt):
    with open(log_file, "a") as f:
        f.write(dt.strftime("%Y-%m-%d %H:%M:%S") + "\n")

async def main():
    await client.start(phone)
    recipient = await client.get_entity(recipient_value)

    # Get all currently scheduled messages from Telegram (best-effort)
    scheduled_msgs = []
    async for msg in client.iter_messages(recipient, limit=200):
        if msg.scheduled and msg.date > datetime.now(tz=sgt):
            scheduled_msgs.append(msg)

    # Normalize Telegram-scheduled datetimes
    scheduled_datetimes_telegram = {
        msg.date.astimezone(sgt).replace(minute=0, second=0, microsecond=0)
        for msg in scheduled_msgs
    }

    # Load from local log file
    scheduled_datetimes_log = load_logged_times()

    # Merge both to avoid duplicates
    all_previously_scheduled = scheduled_datetimes_telegram.union(scheduled_datetimes_log)

    now = datetime.now(sgt)
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    print("Current time SGT:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"Previously scheduled (Telegram + Log): {len(all_previously_scheduled)}")

    messages_scheduled = len(all_previously_scheduled)
    scheduled_time = next_hour

    while messages_scheduled < 100:
        hour = scheduled_time.hour

        # Skip quiet hours
        if 2 <= hour <= 8:
            scheduled_time += timedelta(hours=1)
            continue

        if scheduled_time in all_previously_scheduled:
            print(f"[Skipped] Already scheduled at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} SGT")
        else:
            # Time-specific messages
            if hour == 9:
                message = "Drink up Baby! Please have your breakfast and take your Tribiotix supplement as well!"
            elif hour == 12:
                message = "Drink up Baby! Please have your lunch and take your Yeast B Complex and Vitamin D3 supplements as well!"
            elif hour == 16:
                message = "Drink up Baby! Please have your snack as well!"
            elif hour == 19:
                message = "Drink up Baby! Please have your dinner as well!"
            else:
                message = "Drink Up Baby!"

            try:
                print(f"Scheduling message at: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} SGT")
                await client.send_message(recipient, message=message, schedule=scheduled_time)
                append_logged_time(scheduled_time)
                messages_scheduled += 1
            except Exception as e:
                print(f"[Error] Failed to schedule at {scheduled_time}: {e}")
                break  # stop if hitting a hard limit like ScheduleTooMuchError

        scheduled_time += timedelta(hours=1)

with client:
    client.loop.run_until_complete(main())
