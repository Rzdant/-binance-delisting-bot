import os
import requests
import xml.etree.ElementTree as ET

# Configuration
RSS_URL = "https://binance.com"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Hidden security token
CHANNEL_ID = "-1003704962476"  # Your verified Channel ID

def check_binance_delistings():
    try:
        response = requests.get(RSS_URL, timeout=10)
        if response.status_code != 200:
            print("Failed to fetch Binance RSS feed.")
            return

        root = ET.fromstring(response.content)
        
        # We check the most recent 10 announcements
        for item in root.findall('.//item')[:10]:
            title = item.find('title').text
            link = item.find('link').text
            title_lower = title.lower()
            
            # STRICT FILTER: Check if it's a delisting notice
            if "Binance" in title_lower or "removal of trading pairs" in title_lower:
                message = f"🚨 **BINANCE DELISTING ALERT** 🚨\n\n{title}\n\n🔗 {link}"
                send_telegram_message(message)
                print(f"Match found and sent: {title}")
    except Exception as e:
        print(f"Error checking feed: {e}")

def send_telegram_message(text):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload)
        print(f"Telegram API response: {r.status_code}")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

if __name__ == "__main__":
    check_binance_delistings()
