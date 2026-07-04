import sys
import os
import json
import urllib.request

def process_and_send():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        return
    token = token.strip()
    
    # Grab the raw terminal text output passed from the scanner engine
    raw_html = sys.stdin.read()
    channel_id = "-1003704962476"
    tg_url = f"https://telegram.org{token}/sendMessage"

    # Search for standard Binance delisting strings natively
    if "binance" in raw_html.lower() or "removal of trading pairs" in raw_html.lower():
        # Clean formatting to find target titles inside HTML structures
        alert_text = "🚨 **NEW BINANCE DELISTING ANNOUNCEMENT DETECTED** 🚨\n\nPlease check the official Binance Announcement board immediately."
        
        payload = {
            "chat_id": channel_id,
            "text": alert_text,
            "parse_mode": "Markdown"
        }
        
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(tg_url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"Alert sent successfully. Server code: {resp.getcode()}")
    else:
        print("Scan finished. No new active delisting keywords found in this block.")

if __name__ == "__main__":
    process_and_send()
