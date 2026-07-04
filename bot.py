import os
import requests

# Configuration
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID = "-1003704962476"

def send_test_message():
    print("Attempting to send test message...")
    
    # HARDCODED CORRECT API URL
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {"chat_id": CHANNEL_ID, "text": "🔔 BOT CONNECTION FIXED! 🔔\n\nYour GitHub code and Telegram channel are now perfectly synchronized.", "parse_mode": "Markdown"}
    
    try:
        r = requests.post(url, json=payload)
        print(f"Telegram API response code: {r.status_code}")
        print(f"Telegram API response body: {r.text}")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

if __name__ == "__main__":
    send_test_message()
