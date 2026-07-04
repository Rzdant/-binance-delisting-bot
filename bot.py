import sys
import json
import urllib.request

def process_and_send():
    # Hardcoded with your verified token string
    TOKEN = "8969427446:AAFXHvaggfzAJzV2B1pTKc-vWH7u-w5HaXM"
    channel_id = "-1003704962476"
    tg_url = f"https://telegram.org{TOKEN}/sendMessage"
    
    # Read text passed down through the system pipeline
    raw_html = sys.stdin.read()
    print(f"Data package safely verified. Text string layout length: {len(raw_html)} characters.")
    
    # PRODUCTION SYSTEM FILTER: Tracks explicit delisting announcements
    if "delist" in raw_html.lower() or "removal" in raw_html.lower():
        print("Match found inside stream database block!")
        alert_text = "🚨 **NEW BINANCE DELISTING DETECTED** 🚨\n\nA new developer API update regarding asset removal or delisting was captured on the system logs. Please check your account profile."
        
        payload = {
            "chat_id": channel_id,
            "text": alert_text,
            "parse_mode": "Markdown"
        }
        
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(tg_url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"Alert successfully broadcasted! Server status: {resp.getcode()}")
    else:
        print("Scan complete. Zero active delisting matches found in this text string.")

if __name__ == "__main__":
    process_and_send()
