import sys
import json
import urllib.request

def process_and_send():
    # Fully adjusted with your real API token string
    TOKEN = "8969427446:AAFXHvaggfzAJzV2B1pTKc-vWH7u-w5HaXM"
    channel_id = "-1003704962476"
    tg_url = f"https://telegram.org{TOKEN}/sendMessage"
    
    # Read text straight from the curl terminal pipe
    raw_html = sys.stdin.read()
    print(f"Connection check. Data block length: {len(raw_html)} characters.")
    
    # STRICT PRODUCTION FILTER: Tracks delistings exclusively
    if "delist" in raw_html.lower() or "removal" in raw_html.lower():
        alert_text = "🚨 **NEW BINANCE DELISTING ANNOUNCEMENT** 🚨\n\nA new trading pair removal announcement was detected. Please check the official Binance Announcement board immediately."
        
        payload = {
            "chat_id": channel_id,
            "text": alert_text,
            "parse_mode": "Markdown"
        }
        
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(tg_url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"Alert successfully broadcasted! Server code: {resp.getcode()}")
    else:
        print("Scan complete. Zero delisting matches found in this text string.")

if __name__ == "__main__":
    process_and_send()
